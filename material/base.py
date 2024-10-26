import numpy as np
import imageio

class BaseMaterial:
    def __init__(self, diffuse_path, 
                 normal_path=None, 
                 ao_path=None, 
                 roughness_path=None, 
                 metallic_path=None, 
                 uv_map=None):
        """
        Initialize the BaseMaterial class with the required diffusion texture
        and optional normal, ambient occlusion, roughness, and metallic textures.

        :param diffuse_path: Path to the diffusion (albedo) texture file.
        :param normal_path: Path to the normal map texture file (optional).
        :param ao_path: Path to the ambient occlusion (AO) texture file (optional).
        :param roughness_path: Path to the roughness texture file (optional).
        :param metallic_path: Path to the metallic texture file (optional).
        :param uv_map: Optional list of UV coordinates. Defaults to [(0, 1), (0, 0), (1, 0)].
        """
        # Load diffusion texture (required)
        self.diffuse_texture = self._load_texture(diffuse_path)

        # Initialize optional textures
        self.normal_texture = None
        self.ao_texture = None
        self.roughness_texture = None
        self.metallic_texture = None

        # Load and validate optional textures if paths are provided
        if normal_path:
            self.normal_texture = self._load_texture(normal_path)
            self._validate_texture(self.normal_texture)

        if ao_path:
            self.ao_texture = self._load_texture(ao_path)
            self._validate_texture(self.ao_texture)

        if roughness_path:
            self.roughness_texture = self._load_texture(roughness_path)
            self._validate_texture(self.roughness_texture)

        if metallic_path:
            self.metallic_texture = self._load_texture(metallic_path)
            self._validate_texture(self.metallic_texture)

        # Set the UV map, defaulting to specified coordinates if not provided
        self.uv_map = uv_map if uv_map is not None else np.array([(1, 0), (0, 0), (0, 1)])

    def _load_texture(self, texture_path):
        """
        Load the texture from the file, ensuring it's a 3-channel texture.

        :param texture_path: Path to the texture image file.
        :return: The texture as a numpy array (height, width, 3).
        """
        # Load texture using imageio
        texture = imageio.imread(texture_path)

        # Ensure it's an RGB texture (drop alpha channel if present)
        if texture.shape[2] == 4:
            # Drop the alpha channel (RGBA -> RGB)
            texture = texture[:, :, :3]

        # Check if texture is already 3-channel
        if texture.shape[2] != 3:
            raise ValueError(f"Texture at {texture_path} is not a 3-channel image.")

        return texture

    def _validate_texture(self, texture):
        """
        Validate that the given texture matches the dimensions of the diffusion texture.

        :param texture: Texture array to validate.
        :raises ValueError: If the texture dimensions don't match the diffusion texture.
        """
        if texture.shape != self.diffuse_texture.shape:
            raise ValueError(f"Texture dimensions {texture.shape} do not match diffusion texture dimensions {self.diffuse_texture.shape}")

    # Accessors for the textures

    def get_diffuse_texture(self):
        """
        Get the diffusion texture.
        :return: Diffusion texture as a numpy array.
        """
        return self.diffuse_texture

    def get_normal_texture(self):
        """
        Get the normal texture, if available.
        :return: Normal texture as a numpy array, or None if not set.
        """
        return self.normal_texture

    def get_ao_texture(self):
        """
        Get the ambient occlusion texture, if available.
        :return: Ambient occlusion texture as a numpy array, or None if not set.
        """
        return self.ao_texture

    def get_roughness_texture(self):
        """
        Get the roughness texture, if available.
        :return: Roughness texture as a numpy array, or None if not set.
        """
        return self.roughness_texture

    def get_metallic_texture(self):
        """
        Get the metallic texture, if available.
        :return: Metallic texture as a numpy array, or None if not set.
        """
        return self.metallic_texture

    def get_uv_map(self, face_number=None):
        """
        Get the UV mapping coordinates.

        :param face_number: Optional face index for UV mapping. If None, return the full UV map.
        :return: UV mapping as a numpy array.
        """
        uv_map_shape = self.uv_map.shape

        # Check if uv_map is (3, 2)
        if uv_map_shape == (3, 2):
            return self.uv_map
        
        # Check if uv_map is in the shape of (something, 3, 2)
        elif len(uv_map_shape) == 3 and uv_map_shape[1:] == (3, 2):
            if face_number is None:
                raise ValueError("face_number must be provided when uv_map shape is (N, 3, 2).")
            return self.uv_map[face_number]
        
        else:
            raise ValueError(f"Invalid UV map shape: {uv_map_shape}. Expected shapes are (3, 2) or (N, 3, 2).")

