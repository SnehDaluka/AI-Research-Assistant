import { Box, Typography, Paper } from '@mui/material';
import { GoogleLogin } from '@react-oauth/google';
import { useLoginWithGoogleMutation } from '../api/apiSlice';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';

export default function Login() {
  const [loginWithGoogle] = useLoginWithGoogleMutation();
  const navigate = useNavigate();

  const handleSuccess = async (credentialResponse: any) => {
    try {
      const res = await loginWithGoogle({ credential: credentialResponse.credential }).unwrap();
      localStorage.setItem('token', res.token);
      localStorage.setItem('user', JSON.stringify(res.user));
      navigate('/');
    } catch (err) {
      Swal.fire({
        icon: 'error',
        title: 'Login failed',
        text: 'Could not authenticate with backend.',
        background: '#1e293b',
        color: '#fff'
      });
    }
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', bgcolor: 'background.default', width: '100%' }}>
      <Paper elevation={4} sx={{ p: 5, borderRadius: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', bgcolor: '#0f172a', border: '1px solid rgba(255,255,255,0.05)', maxWidth: 400, width: '100%', mx: 2 }}>
        <img src="/favicon.png" alt="DocMind Logo" style={{ width: 64, height: 64, borderRadius: 16, border: '1px solid rgba(255,255,255,0.2)', boxShadow: '0 0 12px rgba(99, 102, 241, 0.4)', marginBottom: 16 }} />
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 1, background: 'linear-gradient(45deg, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          DocMind
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4, textAlign: 'center' }}>
          Sign in to access your intelligent research assistant and knowledge base.
        </Typography>
        
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={() => {
            Swal.fire({ icon: 'error', title: 'Google Login Failed', background: '#1e293b', color: '#fff' });
          }}
          theme="filled_black"
          shape="circle"
        />
      </Paper>
    </Box>
  );
}
