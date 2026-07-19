import { useRef } from 'react';
import { Button, Box, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import Swal from 'sweetalert2';
import { useUploadDocumentMutation, useClearDocumentsMutation } from '../api/apiSlice';

const Toast = Swal.mixin({
  toast: true,
  position: 'bottom-end',
  showConfirmButton: false,
  timer: 4000,
  timerProgressBar: true,
  background: '#1e293b',
  color: '#fff'
});

export default function DocumentUploader() {
  const [uploadDocument, { isLoading }] = useUploadDocumentMutation();
  const [clearDocuments, { isLoading: isClearing }] = useClearDocumentsMutation();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
    }

    try {
      const res = await uploadDocument(formData).unwrap();
      Toast.fire({
        icon: 'success',
        title: `Indexed ${res.chunks} chunks from ${res.documents} document(s).`
      });
    } catch (err: any) {
      Toast.fire({
        icon: 'error',
        title: err?.data?.detail || 'Upload failed'
      });
    }
    
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClear = () => {
    Swal.fire({
      title: 'Are you sure?',
      text: "This will delete all indexed documents from the knowledge base!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ec4899',
      cancelButtonColor: '#6366f1',
      confirmButtonText: 'Yes',
      background: '#1e293b',
      color: '#fff'
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await clearDocuments().unwrap();
          Toast.fire({ icon: 'success', title: 'Knowledge base cleared.' });
        } catch (err) {
          Toast.fire({ icon: 'error', title: 'Failed to clear knowledge base.' });
        }
      }
    });
  };

  return (
    <Box sx={{ mt: 2 }}>
      <input
        type="file"
        multiple
        hidden
        ref={fileInputRef}
        onChange={handleFileChange}
      />
      <Button
        variant="contained"
        component="span"
        fullWidth
        startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
        disabled={isLoading || isClearing}
        onClick={() => fileInputRef.current?.click()}
        sx={{
            background: 'linear-gradient(45deg, #6366f1 30%, #ec4899 90%)',
            border: 0,
            color: 'white',
            boxShadow: '0 3px 5px 2px rgba(99, 102, 241, .3)',
            transition: 'transform 0.2s',
            '&:hover': { transform: 'scale(1.02)' }
        }}
      >
        {isLoading ? 'Ingesting...' : 'Upload Document'}
      </Button>
      
      <Button
        variant="outlined"
        color="error"
        fullWidth
        startIcon={isClearing ? <CircularProgress size={20} color="inherit" /> : <DeleteSweepIcon />}
        disabled={isLoading || isClearing}
        onClick={handleClear}
        sx={{ mt: 2 }}
      >
        Clear Knowledge Base
      </Button>
    </Box>
  );
}
