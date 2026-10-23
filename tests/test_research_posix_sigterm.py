"""Real POSIX termination controls for both owned verification entry points.

Prepared by JoyboyBrian with OpenAI Codex assistance. Apache-2.0.
Retains Paul Romeo, yssite and ywz65's readiness/ownership test approach.
"""
import json
import os
from pathlib import Path
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]

SOLVER = '''import os, time
from pathlib import Path
Path('solver.pid').write_text(str(os.getpid()))
while not Path('release').exists(): time.sleep(.01)
'''
MODULE = '''import os, subprocess, sys, time, unittest
from pathlib import Path
class T(unittest.TestCase):
    def test_owned_work(self):
        Path('module.pid').write_text(str(os.getpid()))
        child = subprocess.Popen([sys.executable, 'solver.py'])
        while not Path('solver.pid').exists(): time.sleep(.01)
        Path('ready').touch()
        child.wait()
if __name__ == '__main__': unittest.main()
'''
DRIVER = '''import json, os, signal, subprocess, sys, threading, time
from pathlib import Path
sys.path.insert(0, str(Path('scripts').resolve()))
import research_package as package
import run_isolated_tests as isolated
which, mode = sys.argv[1:]
def custom(signum, frame): Path('custom-signal').touch()
if mode == 'custom': signal.signal(signal.SIGTERM, custom)
if mode == 'ignored': signal.signal(signal.SIGTERM, signal.SIG_IGN)
prior = signal.getsignal(signal.SIGTERM)
real_popen = subprocess.Popen
if mode == 'launch':
    def launching(*args, **kwargs):
        process = real_popen(*args, **kwargs)
        while not Path('ready').exists(): time.sleep(.01)
        Path('launch-window').touch()
        while not Path('armed').exists(): time.sleep(.01)
        os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(.05)
        return process
    subprocess.Popen = launching
if mode == 'repeat':
    real_killpg = os.killpg
    def repeated(pid, sig):
        Path('cleanup-signal').touch()
        os.kill(os.getpid(), signal.SIGTERM)
        return real_killpg(pid, sig)
    os.killpg = repeated
def run():
    if which == 'package':
        package.run_python_replay([sys.executable, '-B', 'test_owned.py'], Path.cwd(), 20)
    else:
        results = isolated.run_modules([Path('test_owned.py'), Path('test_z_queued.py')],
                                      tests_dir=Path.cwd(), cwd=Path.cwd(), workers=1)
        if any(code for _, code, _, _ in results): raise RuntimeError('module failed')
if mode == 'thread':
    errors = []
    def worker():
        try: run()
        except BaseException as error: errors.append(error)
    thread = threading.Thread(target=worker)
    thread.start(); thread.join()
    if errors: raise errors[0]
else: run()
if signal.getsignal(signal.SIGTERM) != prior: raise RuntimeError('handler not restored')
print('PASS_HANDLER_RESTORED', flush=True)
'''


def wait_for(predicate, timeout=10):
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() >= deadline:
            raise AssertionError('fixture readiness/exit timeout')
        time.sleep(.01)


class ExitObserver:
    def __init__(self, pid):
        self.exited = False
        if sys.platform == 'linux':
            self.fd = os.pidfd_open(pid)
            self.poll = select.poll()
            self.poll.register(self.fd, select.POLLIN)
        else:
            self.fd = None
            self.kqueue = select.kqueue()
            self.kqueue.control([select.kevent(pid, filter=select.KQ_FILTER_PROC,
                                               flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
                                               fflags=select.KQ_NOTE_EXIT)], 0)

    def stopped(self):
        events = self.poll.poll(0) if self.fd is not None else self.kqueue.control([], 1, 0)
        self.exited = self.exited or bool(events)
        return self.exited

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
        else:
            self.kqueue.close()


@unittest.skipUnless(sys.platform == 'darwin' or
                     (sys.platform == 'linux' and hasattr(os, 'pidfd_open')),
                     'requires native kqueue or Linux pidfd lifetime observations')
class TerminationTests(unittest.TestCase):
    def exercise(self, which, mode='signal'):
        with tempfile.TemporaryDirectory(prefix='posix-term-') as temporary:
            root = Path(temporary)
            (root / 'scripts').mkdir()
            for name in ('research_package.py', 'run_isolated_tests.py'):
                shutil.copyfile(ROOT / 'scripts' / name, root / 'scripts' / name)
            (root / 'solver.py').write_text(SOLVER)
            (root / 'test_owned.py').write_text(MODULE)
            (root / 'test_z_queued.py').write_text(
                "from pathlib import Path\nimport unittest\nclass T(unittest.TestCase):\n"
                " def test_start(self): Path('queued-started').touch()\n")
            (root / 'driver.py').write_text(DRIVER)
            command = [sys.executable, '-B', str(root / 'driver.py'), which, mode]
            process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True)
            observers, pids = [], []
            try:
                wait_for((root / 'ready').exists)
                pids = [int((root / (name + '.pid')).read_text()) for name in ('module', 'solver')]
                observers = [ExitObserver(pid) for pid in pids]
                self.assertFalse(any(observer.stopped() for observer in observers))
                if mode == 'launch':
                    wait_for((root / 'launch-window').exists)
                    (root / 'armed').touch()
                elif mode in ('signal', 'repeat', 'custom', 'ignored'):
                    process.send_signal(signal.SIGTERM)
                if mode == 'custom':
                    wait_for((root / 'custom-signal').exists)
                if mode in ('normal', 'thread', 'custom', 'ignored'):
                    # A retained handler must not cancel work or lose its identity.
                    self.assertIsNone(process.poll())
                    (root / 'release').touch()
                    out, err = process.communicate(timeout=10)
                    self.assertEqual(process.returncode, 0, (out, err))
                    self.assertIn(b'PASS_HANDLER_RESTORED', out)
                else:
                    process.wait(timeout=10)
                    self.assertEqual(process.returncode, 143)
                    self.assertFalse((root / 'queued-started').exists())
                    if mode == 'repeat':
                        self.assertTrue((root / 'cleanup-signal').exists())
                # Observe actual process death before independent fixture teardown.
                wait_for(lambda: all(observer.stopped() for observer in observers), 3)
            finally:
                (root / 'release').touch()
                if pids:
                    try:
                        os.killpg(pids[0], signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                if process.poll() is None:
                    process.kill()
                process.communicate(timeout=5)
                for observer in observers:
                    observer.close()

    def test_registered_replay_terminates_owned_tree(self):
        self.exercise('package')

    def test_isolated_run_terminates_tree_and_cancels_queue(self):
        self.exercise('isolated')

    def test_registered_launch_before_assignment_is_not_lost(self):
        self.exercise('package', 'launch')

    def test_isolated_launch_registers_before_cancellation_snapshot(self):
        self.exercise('isolated', 'launch')

    def test_repeated_signal_does_not_interrupt_cleanup(self):
        for which in ('package', 'isolated'):
            with self.subTest(which=which):
                self.exercise(which, 'repeat')

    def test_existing_custom_and_ignored_handlers_are_preserved(self):
        for which in ('package', 'isolated'):
            for mode in ('custom', 'ignored'):
                with self.subTest(which=which, mode=mode):
                    self.exercise(which, mode)

    def test_normal_completion_restores_default_handler(self):
        for which in ('package', 'isolated'):
            with self.subTest(which=which):
                self.exercise(which, 'normal')

    def test_worker_thread_calls_do_not_install_signal_handlers(self):
        for which in ('package', 'isolated'):
            with self.subTest(which=which):
                self.exercise(which, 'thread')


if __name__ == '__main__':
    unittest.main()
