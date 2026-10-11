"""Distinct JSON encoding, cache lifetime and input-schema contracts."""
import copy
import hashlib
import json
import unittest
from digest_encoder import compile_stream, encoded_records


def reference(events,owners,private):
    for event in events:
        if event[0]==0:
            mapped=[event[0],owners[event[1]],*event[2:]]
        else:
            source=owners[event[2]] if event[2]<len(owners) else private
            mapped=[event[0],owners[event[1]],source,*event[3:]]
        yield (json.dumps(mapped,separators=(',',':'))+'\n').encode()


class DigestEncoderTest(unittest.TestCase):
    def test_json_escaping_integer_tails_and_fresh_owners_per_call(self):
        events=[[0,0,1,2,0,0],[1,0,1,-17,2**130,1],
                [2,0,2,3,4,8,0],[3,0,2,4,3,0,1]]
        owners=[[0,['data','quote"\\\nα',7]],[19,['hosted',3,4,8]]]
        private=[21,['private',0]]
        original=copy.deepcopy([events,owners,private])
        compiled=compile_stream(events)
        first=list(encoded_records(compiled,owners,private))
        self.assertEqual(first,list(reference(events,owners,private)))
        self.assertEqual([events,owners,private],original)
        owners[0][0]=99
        private[0]=100
        second=list(encoded_records(compiled,owners,private))
        self.assertEqual(second,list(reference(events,owners,private)))
        self.assertNotEqual(hashlib.sha256(b''.join(first)).digest(),hashlib.sha256(b''.join(second)).digest())

    def test_rejects_unsupported_schema_and_operand_indices(self):
        for event in [[0,0],[1,0,0],[2,0,1,2,3,4],[3,0,1,2,3,4,False],[4,0,0,0,0,0]]:
            with self.subTest(event=event),self.assertRaises(AssertionError):
                compile_stream([event])
        for event in [[0,-1,0,0,0,0],[1,0,-1,1,0,0],[0,1,0,0,0,0]]:
            with self.subTest(event=event),self.assertRaises(AssertionError):
                list(encoded_records(compile_stream([event]),[[0,['data',0,0]]],[1,['private',0]]))


if __name__=='__main__':
    unittest.main()
