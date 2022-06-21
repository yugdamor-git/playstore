import { Avatar, Box, Button, colors, Grid, Link, Paper, Stack, TextField, Typography } from '@mui/material'
import React from 'react'

const MyApps = () => {

    const data = [
        {
            package_name:"com.whatsapp",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLndoYXRzYXBwX2ljb25fMTU1OTg1MDA2NF8wNjI/icon.png?w=100&fakeurl=1&type=.webp',
            title:'WhatsApp Messenger',
            package_url:'https://m.apkpure.com/whatsapp-messenger/com.whatsapp',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        },
        {
            package_name:"com.instagram.android",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLmluc3RhZ3JhbS5hbmRyb2lkX2ljb25fMTYwNTU3MDIwNF8wNzg/icon.png?w=100&fakeurl=1&type=.webp',
            title:'Instagram',
            package_url:'https://m.apkpure.com/instagram-android/com.instagram.android',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        },
        {
            package_name:"com.whatsapp",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLndoYXRzYXBwX2ljb25fMTU1OTg1MDA2NF8wNjI/icon.png?w=100&fakeurl=1&type=.webp',
            title:'WhatsApp Messenger',
            package_url:'https://m.apkpure.com/whatsapp-messenger/com.whatsapp',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        },
        {
            package_name:"com.instagram.android",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLmluc3RhZ3JhbS5hbmRyb2lkX2ljb25fMTYwNTU3MDIwNF8wNzg/icon.png?w=100&fakeurl=1&type=.webp',
            title:'Instagram',
            package_url:'https://m.apkpure.com/instagram-android/com.instagram.android',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        },
        {
            package_name:"com.whatsapp",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLndoYXRzYXBwX2ljb25fMTU1OTg1MDA2NF8wNjI/icon.png?w=100&fakeurl=1&type=.webp',
            title:'WhatsApp Messenger',
            package_url:'https://m.apkpure.com/whatsapp-messenger/com.whatsapp',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        },
        {
            package_name:"com.instagram.android",
            total_install:"3.5M",
            icon_url:'https://image.winudf.com/v2/image1/Y29tLmluc3RhZ3JhbS5hbmRyb2lkX2ljb25fMTYwNTU3MDIwNF8wNzg/icon.png?w=100&fakeurl=1&type=.webp',
            title:'Instagram Instagram Instagram Instagram Instagram Instagram',
            package_url:'https://m.apkpure.com/instagram-android/com.instagram.android',
            tags:[
                "Tools",
                "Social",
                "Chat"
            ]
        }
    ]



  return (
    <Box>
        <Paper variant='outlined' sx={{bgcolor:'primary.main'}}>
        <Typography variant='h6' color="white.main" textAlign='center'>Recent Apps</Typography>
        </Paper>
        <Box marginTop={2}>
        <TextField fullWidth label='Search Downloaded App' id='search'/>
        </Box>
         <Grid marginTop={1} container spacing={2}
  justifyContent="space-evenly"
  alignItems="center"  columns={{xs:3}}>
        {
            data.map((item,index)=>(

                <Grid marginTop={1} key={index} item>
                    <Link sx={{textDecoration:'none'}}  href='/app/test' >
                    <Stack direction='column' spacing={1} alignItems='center' justifyContent='center' >
                    <Avatar variant="rounded" marginTop={1} marginBottom={1} sx={{ width: 76, height: 76 }} src={item.icon_url}/>
                    <Typography color={colors.grey[600]} width={{xs:'5rem',sm:'7rem',md:'8rem'}} noWrap marginTop={1} fontSize={11} textAlign='center'>{item.title}</Typography>
                    </Stack>
                    </Link>
                </Grid>

            ))
        }
        </Grid>
    </Box>
  )
}

export default MyApps