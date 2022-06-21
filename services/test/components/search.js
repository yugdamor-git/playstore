import { Add } from '@mui/icons-material'
import { Avatar, Box, Divider, IconButton, Link, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Stack, TextField } from '@mui/material'
import React, { useState } from 'react'

const Search = () => {

    const suggestions_test = [
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
        }

    ]

    const [suggestions,setSuggestions] = useState([])

    function fetchSuggestions(keyword)
    {
        return suggestions_test
    }

    function handleSuggestions(input_text)
    {
        if(input_text.length > 0)
        {
            setSuggestions(fetchSuggestions(input_text))
        }
        else{
            setSuggestions([])
        }
    }



  return (
    <Stack>
        <Box>
            <TextField onChange={(e) => handleSuggestions(e.target.value)}  fullWidth label='Search app on apkpure' id='search'/>
        </Box>
        <List>
            {
                suggestions.map((item)=>(
                    <Box>
                    <ListItem
                    disablePadding
                    secondaryAction={
                        <IconButton 
                        sx={{
                            marginRight:1
                        }}
                        edge='end' aria-label='add app'>
                            <Add color='primary'/>
                        </IconButton>
                    }
                    >
                        <ListItemButton>
                            <ListItemIcon>
                                <Avatar src={item.icon_url}/>
                            </ListItemIcon>
                            <ListItemText primary={item.title} secondary={item.package_name} />
                        </ListItemButton>
                        
                    </ListItem>
                    <Divider component="li" />
                    </Box>
                ))
            }
        </List>
    </Stack>
  )
}

export default Search