import { Box, Drawer, List, ListItem, Typography, Divider, Avatar, IconButton } from '@mui/material';
import { Outlet, useNavigate } from 'react-router-dom';
import DocumentUploader from './DocumentUploader';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ChatIcon from '@mui/icons-material/Chat';
import LogoutIcon from '@mui/icons-material/Logout';

const drawerWidth = 280;

export default function Layout() {
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden', bgcolor: 'background.default' }}>
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            backgroundColor: '#0f172a',
            borderRight: '1px solid rgba(255, 255, 255, 0.05)',
          },
        }}
        variant="permanent"
        anchor="left"
      >
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 1.5 }}>
              <AutoAwesomeIcon sx={{ color: '#ec4899' }} />
              <Typography variant="h6" sx={{ fontWeight: 800, background: 'linear-gradient(45deg, #6366f1, #ec4899)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                Research AI
              </Typography>
            </Box>
            <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)' }} />

            {user && (
              <Box sx={{ p: 1.5, display: 'flex', alignItems: 'center', gap: 1.5, m: 2, mb: 0, bgcolor: 'rgba(255,255,255,0.02)', borderRadius: 2, border: '1px solid rgba(255,255,255,0.05)' }}>
                <Avatar src={user.picture || undefined} sx={{ width: 36, height: 36, bgcolor: 'primary.main' }} imgProps={{ referrerPolicy: "no-referrer" }}>
                  {!user.picture && user.name ? user.name.charAt(0).toUpperCase() : ''}
                </Avatar>
                <Box sx={{ overflow: 'hidden', flexGrow: 1 }}>
                  <Typography variant="body2" noWrap sx={{ fontWeight: 600, color: 'text.primary' }}>{user.name}</Typography>
                  <Typography variant="caption" noWrap color="text.secondary" sx={{ display: 'block', mt: -0.2 }}>{user.email}</Typography>
                </Box>
                <IconButton onClick={handleLogout} size="small" sx={{ color: 'text.secondary', '&:hover': { color: '#ef4444', bgcolor: 'rgba(239, 68, 68, 0.1)' } }}>
                  <LogoutIcon fontSize="small" />
                </IconButton>
              </Box>
            )}
            
            <List sx={{ px: 2, pt: 3 }}>
              <ListItem disablePadding>
                 <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, p: 1.5, borderRadius: 2, bgcolor: 'rgba(99, 102, 241, 0.1)', color: 'primary.light', width: '100%', cursor: 'pointer' }}>
                   <ChatIcon fontSize="small" />
                   <Typography variant="body2" sx={{ fontWeight: 600 }}>Active Research</Typography>
                 </Box>
              </ListItem>
            </List>
            
            <Box sx={{ p: 3, mt: 'auto' }}>
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.05)', mb: 3, mx: -3 }} />
              <Typography variant="overline" color="text.secondary" sx={{ fontWeight: 600, letterSpacing: 1, display: 'block' }}>
                KNOWLEDGE BASE
              </Typography>
              <DocumentUploader />
            </Box>
        </Box>
      </Drawer>
      <Box
        component="main"
        sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', height: '100vh', overflow: 'hidden' }}
      >
        <Outlet />
      </Box>
    </Box>
  );
}
