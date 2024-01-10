import torch
import torch.nn as nn

class Encoder(nn.Module):
   def __init__(self, input_dim, hidden_dim, latent_dim):
       super(Encoder, self).__init__()
       self.fc1 = nn.Linear(input_dim, hidden_dim)
       self.fc2 = nn.Linear(hidden_dim, latent_dim)
       
   def forward(self, x):
       h = torch.relu(self.fc1(x))
       return self.fc2(h), self.fc2(h)

class Decoder(nn.Module):
   def __init__(self, latent_dim, hidden_dim, output_dim):
       super(Decoder, self).__init__()
       self.fc1 = nn.Linear(latent_dim, hidden_dim)
       self.fc2 = nn.Linear(hidden_dim, output_dim)
       
   def forward(self, z):
       h = torch.relu(self.fc1(z))
       return torch.sigmoid(self.fc2(h))

class VAE(nn.Module):
   def __init__(self, input_dim, hidden_dim, latent_dim):
       super(VAE, self).__init__()
       self.encoder = Encoder(input_dim, hidden_dim, latent_dim)
       self.decoder = Decoder(latent_dim, hidden_dim, input_dim)
       
   def forward(self, x):
       mu, sigma = self.encoder(x)
       z = self.reparameterize(mu, sigma)
       return self.decoder(z), mu, sigma
   
   @staticmethod
   def reparameterize(mu, sigma):
       std = torch.exp(sigma / 2)
       eps = torch.randn_like(std)
       return mu + eps*std

def vae_loss(recon_x, x, mu, sigma):
   recon_loss = nn.MSELoss()(recon_x, x)
   kld_loss = -0.5 * torch.sum(1 + sigma - mu.pow(2) - sigma.exp())
   return recon_loss + kld_loss
