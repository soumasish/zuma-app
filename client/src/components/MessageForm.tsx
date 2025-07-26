import React from 'react'
import PropertySelect from './PropertySelect'
import BedroomsSelect from './BedroomsSelect'
import DatePicker from './DatePicker'
import type { FormData, Community } from '../types'

interface MessageFormProps {
  formData: FormData
  onSubmit: (e: React.FormEvent) => void
  onInputChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => void
  communities: Community[]
  submitting: boolean
}

const MessageForm: React.FC<MessageFormProps> = ({ formData, onSubmit, onInputChange, communities, submitting }) => {
  return (
    <div className="border-t border-gray-200 p-6">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
            Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={onInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={onInputChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          <PropertySelect 
            value={formData.property} 
            onChange={onInputChange}
            communities={communities}
          />

          <BedroomsSelect 
            value={formData.bedrooms} 
            onChange={onInputChange}
          />

          <DatePicker 
            value={formData.moveInDate} 
            onChange={onInputChange}
          />
        </div>

        <div>
          <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-1">
            Message
          </label>
          <textarea
            id="content"
            name="content"
            value={formData.content}
            onChange={onInputChange}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-y min-h-[80px] max-h-[200px]"
            placeholder="Type your message here..."
            required
          />
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-[#1DA1F2] text-white py-2 px-4 rounded-md hover:bg-[#1a8cd8] focus:outline-none focus:ring-2 focus:ring-[#1DA1F2] focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
        >
          {submitting ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Sending...
            </>
          ) : (
            'Send Message'
          )}
        </button>
      </form>
    </div>
  )
}

export default MessageForm 