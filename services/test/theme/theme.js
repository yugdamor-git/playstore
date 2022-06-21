import React from 'react'
import { Box, createTheme, CssBaseline, Stack, ThemeProvider } from '@mui/material'
import { red } from '@mui/material/colors'
// const colorMode = React.useMemo(
//     () => ({
//       toggleColorMode: () => {
//         setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
//       },
//     }),
//     [],
//   );



export function getTheme(mode)
{
    const theme = React.useMemo(
        () =>
          createTheme({
            palette: {
              mode,
              white:{
                main:"#ffffff"
              },
              primary: {
                main: '#007FFF',
              },
              secondary: {
                main: '#19857b',
              },
              error: {
                main: red.A400,
              },
              text:{
                main:"#1A2027"
              },
              muted:{
                main:"#6F7E8C"
              },
              background:{
                main:"#ffffff"
              },
              shadow:{
                main:"#F3F6F9"
              }
            },
            typography:{
              fontFamily:'"IBM Plex Sans", sans-serif',
            },
            
          }),
        [mode],
      );

    return theme
}
  