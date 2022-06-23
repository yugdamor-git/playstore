import { Add } from '@mui/icons-material'
import { Avatar, Box, Divider, IconButton, Link, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Snackbar, Stack, TextField } from '@mui/material'
import React, { useState } from 'react'
import { backend_base_url } from '../src/config'

const Search = () => {

   
    const [suggestions,setSuggestions] = useState([])

    const [snackbar,setSnackbar] = useState(
        {
            show:false,
            message:""
        }
    )


   async function fetchSuggestions(keyword)
    {
        let url = `${backend_base_url}/get-suggestion?q=${keyword}`
        const response = await fetch(url);
        const json_data = await response.json()
        console.log(json_data)
        return json_data["data"]
    }

    async function handleSuggestions(input_text)
    {
        if(input_text.length >= 3)
        {
            setSuggestions(await fetchSuggestions(input_text))
        }
        else{
            setSuggestions([])
        }
    }

    async function add_app(item)
    {
        let url = `${backend_base_url}/add-application`
        const response = await fetch(url,{
            method:'POST',
            headers: {
                        'Content-Type': 'application/json'
                    },
            body:JSON.stringify({"data":item})
        });
        const json_data = await response.json()
        
        console.log(json_data)
        
        setSnackbar({
            show:true,
            message:json_data.message
        })

        return json_data
    }



  return (
    <Stack>
        <Snackbar
        open={snackbar.show}
        autoHideDuration={3000}
        message={snackbar.message}
        onClick={()=> setSnackbar({show:false,message:""})}
        />
        <Box>
            <TextField onChange={async(e) => handleSuggestions(e.target.value)}  fullWidth label='Search app on apkpure' id='search'/>
        </Box>
        <List>
            {
                suggestions.map((item)=>(
                    <Box>
                    <ListItem
                    disablePadding
                    secondaryAction={
                        <IconButton
                        onClick={()=> add_app(item)}
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