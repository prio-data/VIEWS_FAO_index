import sys
import unittest
import torch

sys.path.insert(0, "/home/simon/Documents/scripts/VIEWS_FAO_index/src/architectures")

from vea_001 import VAE

class TestVAE(unittest.TestCase):
   def setUp(self):
       self.input_dim = 10
       self.hidden_dim = 20
       self.latent_dim = 10
       self.vae = VAE(self.input_dim, self.hidden_dim, self.latent_dim)
       self.test_input = torch.randn((1, self.input_dim))

   def test_init(self):
       self.assertIsInstance(self.vae, VAE)

   def test_forward(self):
       with torch.no_grad():
           output = self.vae(self.test_input)
       self.assertEqual(output[0].shape, (1, self.input_dim))
       self.assertEqual(output[1].shape, (1, self.latent_dim))
       self.assertEqual(output[2].shape, (1, self.latent_dim))

if __name__ == '__main__':
   unittest.main()
