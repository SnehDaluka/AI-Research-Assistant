import { useState, useEffect, useRef } from 'react';
import { Box, IconButton, Paper, Typography, Chip, InputBase } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import SendIcon from '@mui/icons-material/Send';
import StopIcon from '@mui/icons-material/Stop';
import DescriptionIcon from '@mui/icons-material/Description';
import { useCreateSessionMutation, useAskQuestionMutation } from '../api/apiSlice';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

export default function ChatInterface() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [currentRequest, setCurrentRequest] = useState<any>(null);
  
  const [createSession] = useCreateSessionMutation();
  const [askQuestion, { isLoading }] = useAskQuestionMutation();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const initSession = async () => {
      try {
        const res = await createSession().unwrap();
        setSessionId(res.session_id);
      } catch (err) {
        console.error("Failed to create session", err);
      }
    };
    initSession();
  }, [createSession]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage: Message = {
      id: Date.now(),
      type: 'user',
      content: input,
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    const promise = askQuestion({ session_id: sessionId, question: userMessage.content });
    setCurrentRequest(promise);

    try {
      const res = await promise.unwrap();
      const assistantMessage: Message = {
        id: Date.now() + 1,
        type: 'assistant',
        content: res.answer,
        sources: res.sources,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      if (err.name === 'AbortError') {
        setMessages((prev) => [...prev, { id: Date.now() + 1, type: 'assistant', content: 'Generation stopped by user.' }]);
      } else {
        console.error(err);
        setMessages((prev) => [...prev, { id: Date.now() + 1, type: 'assistant', content: 'An error occurred while generating the response.' }]);
      }
    } finally {
      setCurrentRequest(null);
    }
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%', maxWidth: '900px', width: '100%', mx: 'auto' }}>
      <Box sx={{ flexGrow: 1, overflowY: 'auto', p: { xs: 1, sm: 2 }, display: 'flex', flexDirection: 'column', gap: { xs: 1.5, sm: 2 }, '&::-webkit-scrollbar': { width: '8px' }, '&::-webkit-scrollbar-thumb': { backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '4px' } }}>
        {messages.length === 0 && (
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            <Typography variant="h5" color="text.secondary" sx={{ opacity: 0.5 }}>
              What would you like to research today?
            </Typography>
          </Box>
        )}
        {messages.map((msg) => (
          <Box key={msg.id} sx={{ alignSelf: msg.type === 'user' ? 'flex-end' : 'flex-start', maxWidth: msg.type === 'user' ? { xs: '95%', sm: '85%' } : '100%', width: msg.type === 'user' ? 'auto' : '100%' }}>
            <Paper
              elevation={msg.type === 'user' ? 2 : 0}
              sx={{
                p: msg.type === 'user' ? 2 : 0,
                bgcolor: msg.type === 'user' ? 'primary.dark' : 'transparent',
                color: msg.type === 'user' ? 'primary.contrastText' : 'text.primary',
                borderRadius: msg.type === 'user' ? '20px 20px 4px 20px' : 0,
                border: msg.type === 'user' ? '1px solid rgba(255,255,255,0.05)' : 'none'
              }}
            >
              {msg.type === 'user' ? (
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                  {msg.content}
                </Typography>
              ) : (
                <Box sx={{
                  '& p': { m: 0, mb: 1.5, lineHeight: 1.6 },
                  '& p:last-child': { mb: 0 },
                  '& a': { color: 'secondary.light', textDecoration: 'none', '&:hover': { textDecoration: 'underline' } },
                  '& code': { bgcolor: 'rgba(0,0,0,0.2)', p: '2px 6px', borderRadius: 1, fontFamily: 'monospace', fontSize: '0.9em' },
                  '& pre': { bgcolor: 'rgba(0,0,0,0.3)', p: 2, borderRadius: 2, overflowX: 'auto', '& code': { bgcolor: 'transparent', p: 0 } },
                  '& ul, & ol': { m: 0, mb: 1.5, pl: 3 },
                  '& li': { mb: 0.5 },
                  '& h1, & h2, & h3, & h4, & h5, & h6': { mt: 2, mb: 1, fontWeight: 600 },
                  wordBreak: 'break-word',
                  fontSize: '0.95rem'
                }}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.content}
                  </ReactMarkdown>
                </Box>
              )}
              {msg.sources && msg.sources.length > 0 && (
                <Box sx={{ mt: 2, pt: 2, borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                  <Typography variant="caption" color="text.secondary" gutterBottom sx={{ display: 'block', fontWeight: 'bold' }}>
                    Sources
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {msg.sources.map((src, i) => (
                      <Chip
                        key={i}
                        icon={<DescriptionIcon fontSize="small" />}
                        label={`${src.source} (p. ${src.page})`}
                        size="small"
                        variant="outlined"
                        color="secondary"
                        sx={{ fontSize: '0.7rem', borderColor: 'rgba(236, 72, 153, 0.3)' }}
                      />
                    ))}
                  </Box>
                </Box>
              )}
            </Paper>
          </Box>
        ))}
        {isLoading && (
          <Box sx={{ alignSelf: 'flex-start', maxWidth: '80%' }}>
            <Paper elevation={0} sx={{ p: 2, bgcolor: 'transparent' }}>
              <Typography variant="body2" sx={{ display: 'flex', gap: 2, alignItems: 'center', color: 'text.secondary' }}>
                <span className="dot-typing"></span>
              </Typography>
            </Paper>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>

      <Box sx={{ p: { xs: 1, sm: 2 }, bgcolor: 'background.default', mt: 'auto' }}>
        <Paper
          elevation={4}
          sx={{
            display: 'flex',
            alignItems: 'center',
            p: '8px 16px',
            borderRadius: '24px',
            border: '1px solid rgba(255,255,255,0.1)',
            bgcolor: 'rgba(30, 41, 59, 0.8)',
            backdropFilter: 'blur(10px)'
          }}
        >
          <InputBase
            fullWidth
            placeholder="Ask a question about your documents..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend();
                }
            }}
            multiline
            maxRows={4}
            sx={{ flex: 1, ml: 1 }}
            disabled={isLoading || !sessionId}
          />
          {isLoading ? (
            <IconButton color="error" onClick={() => currentRequest?.abort()} sx={{ alignSelf: 'flex-end', mb: 0.5 }}>
              <StopIcon />
            </IconButton>
          ) : (
            <IconButton color="primary" onClick={handleSend} disabled={!input.trim() || !sessionId} sx={{ alignSelf: 'flex-end', mb: 0.5 }}>
              <SendIcon />
            </IconButton>
          )}
        </Paper>
      </Box>
    </Box>
  );
}
