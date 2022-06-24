import { Add } from '@mui/icons-material'
import { Avatar, Box, Divider, IconButton, Link, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Snackbar, Stack, TextField } from '@mui/material'
import { useRouter } from 'next/router'
import React, { useState } from 'react'
import { backend_base_url } from '../src/config'
import { get_auth_token } from '../src/helper'

const Search = () => {

   
    const [suggestions,setSuggestions] = useState([])

    const router = useRouter()

    const [snackbar,setSnackbar] = useState(
        {
            show:false,
            message:""
        }
    )


   async function fetchSuggestions(keyword)
    {
        let url = `${backend_base_url}/get-suggestion?q=${keyword}`
        let auth_token = get_auth_token()
        let headers = {'Content-Type': 'application/json'}
        if(auth_token != undefined)
        {
            headers['Authorization'] = `Bearer ${auth_token}`
        }
        const response = await fetch(url,{
            headers:headers
        });

        const json_data = await response.json()

        if(json_data.auth == false)
        {
            router?.push("/login")
            return
        }

        
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

        let auth_token = get_auth_token()
        let headers = {'Content-Type': 'application/json'}
        if(auth_token != undefined)
        {
            headers['Authorization'] = `Bearer ${auth_token}`
        }


        const response = await fetch(url,{
            method:'POST',
            headers: headers,
            body:JSON.stringify({"data":item})
        });

        const json_data = await response.json()

        if (json_data.auth == false)
        {
            router?.push("/login")
            return
        }
        
        
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