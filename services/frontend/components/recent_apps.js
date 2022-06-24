import { Avatar, Badge, Box, Button, colors, Grid, Link, Paper, Stack, TextField, Typography } from '@mui/material'
import { color } from '@mui/system'
import { useRouter } from 'next/router'
import React, { useState } from 'react'
import { backend_base_url } from '../src/config'
import { get_auth_token } from '../src/helper'

const MyApps = ({data}) => {

  
    const [apps,setApps] = useState(data)

    const router = useRouter()

    async function search_apps(keyword)
    {

        if (keyword.length >= 3)
        {
            backend_base_url
            const url = `${backend_base_url}/search-applications?limit=20&keyword=${keyword}`

            let auth_token = get_auth_token()
            let headers = {}
            if(auth_token != undefined)
            {
                headers['Authorization'] = `Bearer ${auth_token}`
            }

            const response = await fetch(url,{
                headers:headers
            })
            
            const json_data = await response.json()

            if (json_data.auth == false)
            {
                router?.push("/login")
            }


            

            setApps(json_data.data)
        }
        else
        {
            setApps(data)
        }

    }

    return (
        <Box>
            <Paper variant='outlined' sx={{bgcolor:'primary.main'}}>
            <Typography variant='h6' color="white.main" textAlign='center'>Recent Apps</Typography>
            </Paper>
            <Box marginTop={2}>
            <TextField onChange={(e)=>search_apps(e.target.value)} fullWidth label='Search Downloaded App' id='search'/>
            </Box>
            <Grid marginTop={1} container spacing={2}
    justifyContent="space-evenly"
    alignItems="center"  columns={{xs:3}}>
            {
                apps.map((item,index)=>(

                    <Grid marginTop={1} key={index} item>
                        <Link sx={{textDecoration:'none'}}  href={`/app/${item._id}`} >
                        <Stack direction='column' spacing={1} alignItems='center' justifyContent='center' >
                        <Badge color={item.status == "active" ? "success" : "error"}  badgeContent={item.status}>
                        <Avatar variant="rounded" marginTop={1} marginBottom={1} sx={{ width: 76, height: 76 }} src={`${backend_base_url}/icon/${item._id}`}/>
                        </Badge>
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