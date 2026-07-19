import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

export const apiSlice = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ 
    baseUrl: 'http://localhost:8000',
    prepareHeaders: (headers) => {
      const token = localStorage.getItem('token');
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  endpoints: (builder) => ({
    createSession: builder.mutation<{ session_id: string }, void>({
      query: () => ({
        url: '/sessions',
        method: 'POST',
      }),
    }),
    askQuestion: builder.mutation<{ answer: string, sources: any[] }, { session_id: string, question: string }>({
      query: (body) => ({
        url: '/chat',
        method: 'POST',
        body,
      }),
    }),
    uploadDocument: builder.mutation<{ documents: number, chunks: number }, FormData>({
      query: (formData) => ({
        url: '/documents',
        method: 'POST',
        body: formData,
      }),
    }),
    loginWithGoogle: builder.mutation<{ token: string; user: any }, { credential: string }>({
      query: (body) => ({
        url: '/auth/google',
        method: 'POST',
        body,
      }),
    }),
    clearDocuments: builder.mutation<void, void>({
      query: () => ({
        url: '/documents',
        method: 'DELETE',
      }),
    }),
  }),
});

export const {
  useCreateSessionMutation,
  useAskQuestionMutation,
  useUploadDocumentMutation,
  useClearDocumentsMutation,
  useLoginWithGoogleMutation,
} = apiSlice;
