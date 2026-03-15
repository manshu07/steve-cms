/**
 * Image Uploader Component - upload and select images via Cloudinary.
 */

import React, { memo, useState, useCallback, useRef } from 'react';
import {
  Box,
  Button,
  Card,
  CardMedia,
  CardActions,
  Typography,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  TextField,
  IconButton,
} from '@mui/material';
import {
  CloudUpload as CloudUploadIcon,
  Delete as DeleteIcon,
  Image as ImageIcon,
} from '@mui/icons-material';
import { builderApi } from '../../api/builderApi';
import { useNotifications } from '~/hooks/useNotifications';

interface ImageUploaderProps {
  onImageSelect: (imageUrl: string, altText?: string) => void;
  currentImage?: string;
}

export const ImageUploader: React.FC<ImageUploaderProps> = memo(({ onImageSelect, currentImage }) => {
  const { showSuccess, showError } = useNotifications();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [isUploading, setIsUploading] = useState(false);
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch user's uploaded assets
  const { data: assets = [], isLoading } = builderApi.getUserAssets.useQuery();

  // Handle file selection
  const handleFileSelect = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      showError('Please select an image file', 'Invalid File');
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      showError('Image file must be less than 5MB', 'File Too Large');
      return;
    }

    setIsUploading(true);

    try {
      // Upload to Cloudinary via Django API
      const uploadedAsset = await builderApi.uploadBuilderAsset(file, {
        alt_text: file.name,
        width: 1200,
      });

      showSuccess('Image uploaded successfully!', 'Upload Success');
      onImageSelect(uploadedAsset.file, uploadedAsset.metadata?.alt_text);
      setOpen(false);
    } catch (error) {
      console.error('Upload failed:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      showError(`Failed to upload image: ${errorMessage}`, 'Upload Error');
    } finally {
      setIsUploading(false);
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, [onImageSelect, showSuccess, showError]);

  // Handle image selection from library
  const handleSelectImage = useCallback((imageUrl: string, altText?: string) => {
    onImageSelect(imageUrl, altText);
    setOpen(false);
  }, [onImageSelect]);

  // Handle delete current image
  const handleDeleteCurrent = useCallback(() => {
    onImageSelect('', '');
  }, [onImageSelect]);

  // Open modal
  const handleOpen = useCallback(() => {
    setOpen(true);
  }, []);

  // Close modal
  const handleClose = useCallback(() => {
    setOpen(false);
  }, []);

  return (
    <>
      {/* Current Image Display */}
      <Box sx={{ mb: 2 }}>
        {currentImage ? (
          <Card>
            <CardMedia
              component="img"
              image={currentImage}
              alt="Current image"
              sx={{ height: 200, objectFit: 'contain' }}
            />
            <CardActions>
              <Button
                size="small"
                startIcon={<CloudUploadIcon />}
                onClick={handleOpen}
              >
                Change Image
              </Button>
              <Button
                size="small"
                color="error"
                startIcon={<DeleteIcon />}
                onClick={handleDeleteCurrent}
              >
                Remove
              </Button>
            </CardActions>
          </Card>
        ) : (
          <Box
            sx={{
              border: 2,
              borderColor: 'divider',
              borderRadius: 1,
              p: 4,
              textAlign: 'center',
              bgcolor: 'background.default',
            }}
          >
            <ImageIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
            <Typography variant="body2" color="text.secondary" gutterBottom>
              No image selected
            </Typography>
            <Button
              variant="outlined"
              startIcon={<CloudUploadIcon />}
              onClick={handleOpen}
              sx={{ mt: 1 }}
            >
              Upload Image
            </Button>
          </Box>
        )}
      </Box>

      {/* Upload Button (Hidden Input) */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={handleFileSelect}
      />

      {/* Image Library Modal */}
      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>Choose an Image</DialogTitle>

        <DialogContent>
          {/* Upload New Image */}
          <Box sx={{ mb: 3, p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
            <Typography variant="subtitle2" gutterBottom>
              Upload New Image
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
              <Button
                variant="outlined"
                startIcon={<CloudUploadIcon />}
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading}
              >
                {isUploading ? 'Uploading...' : 'Choose File'}
              </Button>
              {isUploading && <CircularProgress size={24} />}
              <Typography variant="caption" color="text.secondary">
                JPG, PNG, GIF up to 5MB
              </Typography>
            </Box>
          </Box>

          {/* Search */}
          <TextField
            fullWidth
            size="small"
            placeholder="Search images..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ mb: 2 }}
          />

          {/* Image Library */}
          {isLoading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          ) : assets.length === 0 ? (
            <Alert severity="info">No images uploaded yet</Alert>
          ) : (
            <Grid container spacing={1}>
              {assets
                .filter((asset: any) =>
                  !searchQuery ||
                  asset.original_filename?.toLowerCase().includes(searchQuery.toLowerCase())
                )
                .map((asset: any) => (
                  <Grid size={{ xs: 4, sm: 3, md: 2 }} key={asset.id}>
                    <Card
                      sx={{
                        cursor: 'pointer',
                        '&:hover': {
                          boxShadow: 4,
                        },
                      }}
                      onClick={() => handleSelectImage(asset.file, asset.metadata?.alt_text)}
                    >
                      <CardMedia
                        component="img"
                        image={asset.file}
                        alt={asset.original_filename}
                        sx={{ height: 80, objectFit: 'cover' }}
                      />
                    </Card>
                  </Grid>
                ))}
            </Grid>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </>
  );
});

ImageUploader.displayName = 'ImageUploader';

export default ImageUploader;
