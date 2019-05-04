import torch
import torch.nn as nn
import unittest

from torchvision import transforms as T
from scratchai import *

class TestOneCalls(unittest.TestCase):
  
  url_1 = 'https://cdn.instructables.com/FVI/FJPH/FWYHRVGC/FVIFJPHFWYHRVGC.LARGE.jpg'
  lab_1 = 'rain barrel'

  url_2 = 'http://bradleymitchell.me/wp-content/uploads/2014/06/decompressed.jpg'
  lab_2 = 'five'

  def test_classify(self):
    """
    This function ensures the classify function is working properly.
    """
    # Check that url works.
    pred, val = one_call.classify(TestOneCalls.url_1)
    self.assertTrue(isinstance(pred, str), 'Doesn\'t Work!')
    self.assertTrue(pred == TestOneCalls.lab_1, 'Doesn\'t Work!')

    # TODO Check that path in local works

    # Check that mnist works
    pred, val = one_call.classify(TestOneCalls.url_2, nstr='lenet_mnist', trf='rz32_cc28_tt')
    self.assertTrue(isinstance(pred, str), 'Doesn\'t Work!')
    self.assertTrue(pred == TestOneCalls.lab_2, 'Doesn\'t Work!')

  def test_stransfer(self):
    """
    Ensures the stransfer function is working properly.
    """
    imgshape = T.ToTensor()(imgutils.load_img(TestOneCalls.url_1)).shape
    simgshape = T.ToTensor()(one_call.stransfer(TestOneCalls.url_1, show=False)).shape
    self.assertTrue(imgshape == simgshape, 'doesn\'t look good')