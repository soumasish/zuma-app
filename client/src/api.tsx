import axios from 'axios'
import type { Community, ReplyRequest, ReplyResponse } from './types'

const API_BASE_URL = 'http://localhost:9000'

export const fetchCommunities = async (): Promise<Community[]> => {
  try {
    console.log('Fetching communities...')
    const response = await axios.get(`${API_BASE_URL}/api/communities`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    console.log('Response status:', response.status)
    console.log('Response headers:', response.headers)
    console.log('Response data type:', typeof response.data)
    console.log('Response data:', response.data)
    
    return response.data
  } catch (error) {
    console.error('Error fetching communities:', error)
    throw error
  }
}

export const sendReply = async (requestData: ReplyRequest): Promise<ReplyResponse> => {
  try {
    console.log('Sending reply request...')
    const response = await axios.post(`${API_BASE_URL}/api/reply`, requestData, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    console.log('Reply response:', response.data)
    return response.data
  } catch (error) {
    console.error('Error sending reply:', error)
    throw error
  }
} 