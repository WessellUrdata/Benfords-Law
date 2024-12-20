import torch
import torchvision.transforms.functional


def azimuthalAverage(magnitude_spectrum: torch.Tensor) -> torch.Tensor:
    device = magnitude_spectrum.device

    height, width = magnitude_spectrum.size(1), magnitude_spectrum.size(2)

    # Calculate the indices from the image
    y, x = torch.meshgrid(
        torch.arange(height, device=device),
        torch.arange(width, device=device),
        indexing="ij",
    )

    center_y, center_x = (
        torch.tensor((height - 1) / 2, device=device),
        torch.tensor((width - 1) / 2, device=device),
    )

    r = torch.hypot(y - center_y, x - center_x)

    # Get the integer part of the radii (bin size = 1)
    r_int = r.to(torch.int16)

    # Calculate the mean for each radius bin
    tbin = torch.bincount(r_int.view(-1), magnitude_spectrum.view(-1))
    nr = torch.bincount(r_int.view(-1))

    radial_prof = tbin / nr

    return radial_prof


class FeatureExtraction:
    def __init__(self, features: int = 100):
        self.features = features

    def fft(
        self,
        img: torch.Tensor,
        crop: bool = True,
    ):
        height, width = img.size(dim=1), img.size(dim=2)

        if crop:
            # crop to the center one-third of the image
            img = torchvision.transforms.functional.crop(
                img,
                height // 3,
                width // 3,
                height // 3,
                width // 3,
            )

        # do FFT
        frequencies = torch.fft.fft2(img)
        # shift zero frequency component to center
        # not doing frequency shift will slightly negatively impact accuracy
        frequencies = torch.fft.fftshift(frequencies)

        # calculate magnitude spectrum
        magnitude_spectrum = torch.abs(frequencies)

        # Calculate the azimuthally averaged 1D power spectrum
        psd1D = azimuthalAverage(magnitude_spectrum)

        return psd1D
