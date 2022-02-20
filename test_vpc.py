import unittest
from typing import Tuple, Optional, List
import pulumi

class testMocks(pulumi.runtime.Mocks):
  def new_resource(self, args: pulumi.runtime.MockResourceArgs) -> Tuple[Optional[str], dict]:
    return super().new_resource(args)
  def call(self, args: pulumi.runtime.MockCallArgs) -> Tuple[dict, Optional[List[Tuple[str, str]]]]:
    return super().call(args)

pulumi.runtime.set_mocks(testMocks())

import network
