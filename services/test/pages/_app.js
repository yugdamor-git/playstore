import React from 'react';
import { CacheProvider } from '@emotion/react';
import PropTypes from 'prop-types';
import createEmotionCache from '../src/createEmotionCache';
import Layout from '../components/layout';
import Navbar from '../components/navbar';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { getTheme } from '../theme/theme';

const clientSideEmotionCache = createEmotionCache();

const MyApp = (props) => {
 const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;

 const [mode, setMode] = React.useState('light');

 const colorMode = React.useMemo(
  () => ({
    toggleColorMode: () => {
      setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
    },
  }),
  [],
);

 return (
   
   <CacheProvider value={emotionCache}>
     {/* <ThemeProvider theme={theme}>
       <CssBaseline /> */}
       <ThemeProvider theme={getTheme(mode)}>
       <CssBaseline />
       <Layout>
       <Component {...pageProps} />
       </Layout>
       </ThemeProvider>
     {/* </ThemeProvider> */}
   </CacheProvider>
 );
};

export default MyApp;

MyApp.propTypes = {
  Component: PropTypes.elementType.isRequired,
  emotionCache: PropTypes.object,
  pageProps: PropTypes.object.isRequired,
 };