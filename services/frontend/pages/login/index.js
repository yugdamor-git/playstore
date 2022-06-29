import { LoginOutlined } from '@mui/icons-material'
import { Button, Snackbar, Stack, TextField, Typography } from '@mui/material'
import { useRouter } from 'next/router'
import React, { useState } from 'react'
import { backend_base_url, token } from '../../src/config'
import { get_auth_token, set_auth_token } from '../../src/helper'

const Login = () => {

    const router = useRouter()

    const [snackbar,setSnackbar] = useState(
        {
            show:false,
            message:""
        }
    )

    const [username,setUsername] = useState('')
    const [password,setPassword] = useState('')

    async function login_request(username,password)
    {
        if (username == '')
        {
            setSnackbar({show:true,message:"please enter username"})
            return
        }

        if (password == '')
        {
            setSnackbar({show:true,message:"please enter password"})
            return
        }
        const url = `${backend_base_url}/auth`
        let data = {
            'email':username,
            'password':password
        }
        const response = await fetch(url,{
            headers:{
                'Content-Type': 'application/json'
            },
            method:'POST',
            body:JSON.stringify({'data':data})
        })

        const json_data = await response.json()

        if (json_data.status == false)
        {
            setSnackbar({show:true,message:json_data.message})
        }
        else{
            const auth_token = json_data["data"]["token"]
            set_auth_token(auth_token)
            router.push('/home')

        }

    }



  return (
   <Stack height="60vh" display="flex" flexDirection="column" justifyContent={'center'} alignItems='center'>
    <Snackbar
        open={snackbar.show}
        autoHideDuration={3000}
        message={snackbar.message}
        onClick={()=> setSnackbar({show:false,message:""})}
        />
        <Stack spacing={4} justifyContent={'center'} alignItems='center'>
            <Typography textAlign='center' fontWeight={800} fontSize={30} color='primary' >Welcome to App Manager</Typography>
            <Typography textAlign='center' fontWeight={600} fontSize={30}  >Login</Typography>
            <TextField value={username} onChange={(e=>setUsername(e.target.value))} label='Username'/>
            <TextField value={password} onChange={(e=>setPassword(e.target.value))} type="password" label='Password'/>
            <Button onClick={async() => login_request(username,password)} variant='outlined' startIcon={<LoginOutlined/>}>
                Sign In
            </Button>
        </Stack>
   </Stack>
  )
}

export default Login


export async function getServerSideProps(context) {

    const cookies = context.req.cookies
    
    const auth_token = cookies["auth_token"]

    if(auth_token != null)
    {
        return {
            redirect: {
              permanent: false,
              destination: "/home"
            }
      }
    }


    const id = context.query.token

    if (id == null || id != token)
    {
        return {
            notFound: true,
          }
    }
    else {

        return {
            props:{}
        }
    }
  }

