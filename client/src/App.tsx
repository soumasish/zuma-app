import { useState, useEffect } from 'react'
import './App.css'
import ChatDisplay from './components/ChatDisplay'
import MessageForm from './components/MessageForm'
import { fetchCommunities, sendReply } from './api'
import type { ChatMessage, FormData, Community } from './types'

function App() {
  const [chats, setChats] = useState<ChatMessage[]>([])
  const [communities, setCommunities] = useState<Community[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    content: '',
    property: '',
    bedrooms: 0,
    moveInDate: ''
  })

  useEffect(() => {
    const loadCommunities = async () => {
      try {
        const data = await fetchCommunities()
        setCommunities(data)
      } catch (error) {
        console.error('Error loading communities:', error)
        setCommunities([])
      } finally {
        setLoading(false)
      }
    }

    loadCommunities()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validation
    if (!formData.name || !formData.email || !formData.content || !formData.property) {
      console.error('All fields are required')
      return
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(formData.email)) {
      console.error('Invalid email format')
      return
    }
    
    setSubmitting(true)
    
    try {
      const requestData = {
        lead: {
          name: formData.name,
          email: formData.email
        },
        message: formData.content,
        preferences: {
          bedrooms: formData.bedrooms,
          move_in: formData.moveInDate
        },
        community_id: formData.property
      }
      
      const response = await sendReply(requestData)
      console.log('API Response:', response)
      
      // Add user message to chat display
      const userChat: ChatMessage = {
        id: Date.now().toString(),
        name: formData.name,
        email: formData.email,
        content: formData.content,
        property: formData.property,
        bedrooms: formData.bedrooms,
        moveInDate: formData.moveInDate,
        timestamp: new Date()
      }
      
      // Add API reply to chat display
      const replyChat: ChatMessage = {
        id: (Date.now() + 1).toString(),
        name: 'Assistant',
        email: 'assistant@zuma.com',
        content: response.message || response.reply || 'No message content',
        property: formData.property,
        action: response.action,
        timestamp: new Date()
      }
      
      setChats([...chats, userChat, replyChat])
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        content: '',
        property: '',
        bedrooms: 0,
        moveInDate: ''
      })
    } catch (error) {
      console.error('Error submitting form:', error)
    } finally {
      setSubmitting(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex justify-center items-center">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-start pt-8">
      <div className="w-full sm:w-96 md:w-1/3 max-w-md bg-white rounded-lg shadow-lg h-[calc(100vh-4rem)] flex flex-col">
        <ChatDisplay chats={chats} />
        <MessageForm 
          formData={formData}
          onSubmit={handleSubmit}
          onInputChange={handleInputChange}
          communities={communities}
          submitting={submitting}
        />
      </div>
    </div>
  )
}

export default App
