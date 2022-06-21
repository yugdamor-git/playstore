import { Avatar, Button, colors, Divider, Icon, IconButton, Link, List, ListItem, ListItemText, Paper, Stack, TextField, Typography } from '@mui/material'
import { Box } from '@mui/system'
import React from 'react'
import DownloadIcon from '@mui/icons-material/Download';
import DeleteIcon from '@mui/icons-material/Delete';

const AppDetails = () => {


    const data =  {
        package_name:"com.instagram.android",
        total_install:"3.5M",
        icon_url:'https://image.winudf.com/v2/image1/Y29tLmluc3RhZ3JhbS5hbmRyb2lkX2ljb25fMTYwNTU3MDIwNF8wNzg/icon.png?w=100&fakeurl=1&type=.webp',
        title:'Instagram',
        package_url:'https://m.apkpure.com/instagram-android/com.instagram.android',
        tags:[
            "Tools",
            "Social",
            "Chat"
        ],
        description:"Welcome to the world of easylearning sewing and complete delight. All you need is to relax and enjoy sewing different wares. With each level, your logic and skills are pumped more and more. You have absolute freedom of action, do what you want and earn money! Upgrade your skill and become a real professional!"
    }


    const versions = [

        {
            title:"Instagram v1.1.1",
            version:'v1.1.1',
            size:'58Mb',
            version_code:'8883883',
            download_url:'https://',
            updated_at:'28-06-2022',
            type:'Apk',
            variant:false
        },
        {
            title:"Instagram v1.1.1",
            version:'v1.1.1',
            size:'58Mb',
            version_code:'8883883',
            download_url:'https://',
            updated_at:'28-06-2022',
            type:'Apk',
            variant:false
        },
        {
            title:"Instagram v1.1.1",
            version:'v1.1.1',
            size:'58Mb',
            version_code:'8883883',
            download_url:'https://',
            updated_at:'28-06-2022',
            type:'Apk',
            variant:false
        },
        {
            title:"Instagram v1.1.1",
            version:'v1.1.1',
            size:'58Mb',
            version_code:'8883883',
            download_url:'https://',
            updated_at:'28-06-2022',
            type:'Apk',
            variant:false
        },
        {
            title:"Instagram v1.1.1",
            version:'v1.1.1',
            size:'58Mb',
            version_code:'8883883',
            download_url:'https://',
            updated_at:'28-06-2022',
            type:'Apk',
            variant:false
        }
    ]
  return (
    <Box>
        <Stack direction={'column'}>
            <Stack alignItems='center'  direction={'row'}>
                <Avatar variant='rounded' sx={{ width: 85, height: 85 }} src={data.icon_url}/>
                <Stack marginX={{xs:4}}>
                <Typography fontSize={20} color={colors.grey[700]} fontWeight={600}>{data.title}</Typography>
                <Typography>{data.package_name}</Typography>
                <Typography>{data.total_install}</Typography>
                <Link target='_blank' href={data.package_url}>
                    <Typography>View On Apkpure</Typography>
                </Link>
                </Stack>
            
            </Stack>
            
            <Stack alignItems='center' spacing={2} marginY={2}>
                <Button fullWidth variant='contained' color={'error'} startIcon={<DeleteIcon/>}>Delete App</Button>
                <Button fullWidth variant='contained' startIcon={<DownloadIcon/>}>Download Latest Apk Version</Button>
            </Stack>

            

            <Box>
            <Stack>
                    <Typography p={1} fontWeight={600} color={"primary"} textAlign='center'>App Description</Typography>
                    <TextField
                    multiline
                    maxRows={10}
                    defaultValue={data.description}
                    >
                    </TextField>
                    <Box marginY={2}>
                    <Button size={"small"} variant='outlined'>Update App Description</Button>
                    </Box>
                </Stack>
            </Box>
            
            <Stack>
                <Paper elevation={0} variant="outlined">
                    <Typography p={1} fontWeight={600} textAlign='center'>App Versions</Typography>
                </Paper>
                <List>
                    {
                        versions.map((item,index)=>(
                            <Box marginY={2}>
                                <Paper elevation={1}>
                                    <ListItem
                                    secondaryAction={
                                        <IconButton>
                                            <DownloadIcon/>
                                        </IconButton>
                                    }
                                    key={index}>
                                        <ListItemText primary={item.title} secondary={`${item.updated_at} - ${item.size} - ${item.type}`}/>

                                    </ListItem>

                                </Paper>
                            </Box>
                        ))
                    }
                </List>
            </Stack>

        </Stack>
    </Box>
  )
}

export default AppDetails