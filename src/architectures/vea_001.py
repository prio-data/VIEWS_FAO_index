import torch
import torch.nn as nn


class Encoder(nn.Module):
    def __init__(self, input_dim = 128, input_channels = 1, hidden_channels = 8):
        super(Encoder, self).__init__()

        latent_dim = hidden_channels*8 * int(input_dim/16) * int(input_dim/16) # defualt 4096 since input_dim = 128 and hidden_channels = 8

        self.conv1 = nn.Conv2d(input_channels, hidden_channels, kernel_size=4, stride=2, padding=1) # with defualt settings: 1x128x128 ->  8x64x64
        self.conv2 = nn.Conv2d(hidden_channels, hidden_channels*2, kernel_size=4, stride=2, padding=1) # 8x64x64 -> 16x32x32
        self.conv3 = nn.Conv2d(hidden_channels*2, hidden_channels*4, kernel_size=4, stride=2, padding=1) # 16x32x32 -> 32x16x16
        self.conv4 = nn.Conv2d(hidden_channels*4, hidden_channels*8, kernel_size=4, stride=2, padding=1) # 32x16x16 -> 64x8x8

        self.fc_mean = nn.Linear(latent_dim, latent_dim) # 4096 -> 4096
        self.fc_logvar = nn.Linear(latent_dim, latent_dim) # 4096 -> 4096

    def forward(self, x):

        h = torch.relu(self.conv1(x))
        h = torch.relu(self.conv2(h))
        h = torch.relu(self.conv3(h))
        h = torch.relu(self.conv4(h))
        
        h = h.view(h.size(0), -1) # flatten to 1D, but keep batch size
        
        mean = self.fc_mean(h)
        logvar = torch.exp(self.fc_logvar(h))
        
        return mean, logvar


class Decoder(nn.Module):
    def __init__(self, input_dim = 128, output_channels = 1, hidden_channels = 8):
        super(Decoder, self).__init__()

        self.pre_latent_dim = (1, hidden_channels*8, int(input_dim/16), int(input_dim/16)) # so if default back to 64x8x8 

        self.deconv1 = nn.ConvTranspose2d(hidden_channels*8, hidden_channels*4, kernel_size=4, stride=2, padding=1) # 
        self.deconv2 = nn.ConvTranspose2d(hidden_channels*4, hidden_channels*2, kernel_size=4, stride=2, padding=1) # 
        self.deconv3 = nn.ConvTranspose2d(hidden_channels*2, hidden_channels, kernel_size=4, stride=2, padding=1) # 
        self.deconv4 = nn.ConvTranspose2d(hidden_channels, output_channels, kernel_size=4, stride=2, padding=1) # 

    def forward(self, z):
        
        z  = z.view(*self.pre_latent_dim) 
        h = torch.relu(self.deconv1(z))
        h = torch.relu(self.deconv2(h))
        h = torch.relu(self.deconv3(h))
        h = torch.relu(self.deconv4(h))
        return h 


class VAE(nn.Module):
   def __init__(self, input_dim = 128, input_channels = 1, hidden_channels = 8, output_channels = 1):
       super(VAE, self).__init__()
       self.encoder = Encoder(input_dim, input_channels, hidden_channels)
       self.decoder = Decoder(input_dim, output_channels, hidden_channels)

   def forward(self, x):
       mean, logvar = self.encoder(x)
       z = self.reparameterize(mean, logvar)
       return self.decoder(z), mean, logvar

   @staticmethod
   def reparameterize(mean, logvar):
       std = torch.exp(logvar / 2)
       eps = torch.randn_like(std)
       return mean + eps*std


# def vae_loss(recon_x, x, mean, logvar):
#    criterion = nn.BCEWithLogitsLoss(reduction='sum')
#    BCE = criterion(recon_x, x)
# 
#    # see Appendix B from VAE paper:
#    # Kingma and Welling. Auto-Encoding Variational Bayes. ICLR, 2014
#    # https://arxiv.org/abs/1312.6114
#    # 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
#    KLD = -0.5 * torch.sum(1 + logvar - mean.pow(2) - logvar.exp())
# 
#    return BCE + KLD

def latent_loss(mean, logvar):
    # KLD = -0.5 * torch.sum(1 + logvar - mean.pow(2) - logvar.exp(), dim=1)
    kld_loss = nn.KLDivLoss(reduction='sum')
    KLD = kld_loss(mean, logvar)
    return KLD

def reconstruction_loss(x_reconstructed, x):
    mse_loss = nn.MSELoss(reduction='sum')
    MSE =  mse_loss(x_reconstructed, x)
    return MSE

def vae_loss(recon_x, x, mu, logvar):
    recon_loss = reconstruction_loss(recon_x, x)
    kld_loss = latent_loss(mu, logvar)
    return recon_loss + kld_loss
# 
























