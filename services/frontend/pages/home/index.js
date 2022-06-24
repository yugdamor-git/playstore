import { Box } from '@mui/material'
import { useRouter } from 'next/router'
import React from 'react'
import MyApps from '../../components/recent_apps'
import Search from '../../components/search'
import { backend_base_url } from '../../src/config'
import { get_auth_token } from '../../src/helper'

const Home = ({data}) => {

    // const router = useRouter()


    // async function fetch_recent_apps()
    // {
  
    //   let auth_token = get_auth_token()
    //   let headers = {}
    //   if(auth_token != undefined)
    //   {
    //       headers['Authorization'] = `Bearer ${auth_token}`
    //   }
      
    //   const response = await fetch(`${backend_base_url}/get-recent-application?limit=15`,{
    //     headers:headers
    //   })
  
    //   if (response.status == 401)
    //   {
    //     router?.push("/login")
    //     return
    //   }
  
    //   const data = await response.json()
    //   return data["data"]
    // }


    let [recentApps,setRecentApps] = React.useState(data)
  
  
    // React.useEffect(() => {

    //   let recent_apps = fetch_recent_apps()
    //   setRecentApps(recent_apps)
    // },[])


  return (
    <Box>
     <Search/>
     {recentApps &&
      <MyApps data={recentApps} />
     }
     
    </Box>
  )
}

export default Home


export async function getServerSideProps(context) {

    const cookies = context.req.headers.cookie;

    const auth_token = cookies["auth_token"]
    let headers = {}
    if(auth_token != undefined)
      {
          headers['Authorization'] = `Bearer ${auth_token}`
      }
      
      const response = await fetch(`${backend_base_url}/get-recent-application?limit=15`,{
        headers:headers
      })
      
      const data = await response.json()

      if(response.auth == False)
      {
        return {
            redirect: {
              permanent: false,
              destination: "/login"
            }
      }
    }

    return {
      props: {
        "data":data["data"]
      }, // will be passed to the page component as props
    }
  }