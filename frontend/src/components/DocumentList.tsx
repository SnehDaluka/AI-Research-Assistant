import { Box, CircularProgress, List, ListItem, ListItemIcon, ListItemText, Typography, Button, IconButton } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';
import DeleteIcon from '@mui/icons-material/Delete';
import Swal from 'sweetalert2';
import { useGetDocumentsQuery, useClearDocumentsMutation, useDeleteDocumentMutation } from '../api/apiSlice';

const Toast = Swal.mixin({
  toast: true,
  position: 'bottom-end',
  showConfirmButton: false,
  timer: 4000,
  timerProgressBar: true,
  background: '#1e293b',
  color: '#fff'
});

export default function DocumentList() {
  const { data: docsData, isLoading: isLoadingDocs } = useGetDocumentsQuery();
  const [clearDocuments, { isLoading: isClearing }] = useClearDocumentsMutation();
  const [deleteDocument, { isLoading: isDeleting }] = useDeleteDocumentMutation();

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
      color: '#fff',
      customClass: {
        container: 'swal2-container'
      }
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

  const handleDelete = (filename: string) => {
    Swal.fire({
      title: 'Delete Document?',
      text: `Are you sure you want to delete ${filename}?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ec4899',
      cancelButtonColor: '#6366f1',
      confirmButtonText: 'Yes, delete it',
      background: '#1e293b',
      color: '#fff',
      customClass: {
        container: 'swal2-container'
      }
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          await deleteDocument(filename).unwrap();
          Toast.fire({ icon: 'success', title: 'Document removed.' });
        } catch (err) {
          Toast.fire({ icon: 'error', title: 'Failed to remove document.' });
        }
      }
    });
  };

  return (
    <Box sx={{ mt: 2 }}>
      {isLoadingDocs ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
          <CircularProgress size={24} />
        </Box>
      ) : (
        docsData?.documents && docsData.documents.length > 0 ? (
          <List sx={{ mb: 2, bgcolor: 'rgba(255,255,255,0.02)', borderRadius: 2, p: 1, border: '1px solid rgba(255,255,255,0.05)', maxHeight: 'calc(100vh - 200px)', overflowY: 'auto' }}>
            {docsData.documents.map((doc, idx) => (
              <ListItem 
                key={idx} 
                disablePadding 
                sx={{ py: 0.5 }}
                secondaryAction={
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(doc)} disabled={isDeleting} sx={{ color: 'text.secondary', '&:hover': { color: '#ef4444', bgcolor: 'rgba(239, 68, 68, 0.1)' } }}>
                    <DeleteIcon fontSize="small" />
                  </IconButton>
                }
              >
                <ListItemIcon sx={{ minWidth: 32 }}>
                  <PictureAsPdfIcon fontSize="small" sx={{ color: '#ec4899' }} />
                </ListItemIcon>
                <ListItemText 
                  primary={doc} 
                  primaryTypographyProps={{ variant: 'caption', sx: { color: 'text.secondary', fontWeight: 500, wordBreak: 'break-all', pr: 3 } }}
                />
              </ListItem>
            ))}
          </List>
        ) : (
          <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', mb: 2, mt: 2 }}>
            No documents uploaded.
          </Typography>
        )
      )}

      {docsData?.documents && docsData.documents.length > 0 && (
        <Button
          variant="outlined"
          color="error"
          fullWidth
          startIcon={isClearing ? <CircularProgress size={20} color="inherit" /> : <DeleteSweepIcon />}
          disabled={isClearing}
          onClick={handleClear}
          sx={{ mt: 2 }}
        >
          Clear Knowledge Base
        </Button>
      )}
    </Box>
  );
}
