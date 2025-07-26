import React from 'react'
import type { ChatMessage } from '../types'

interface ChatDisplayProps {
  chats: ChatMessage[]
}

const ChatDisplay: React.FC<ChatDisplayProps> = ({ chats }) => {
  return (
    <div className="flex-1 p-6 overflow-y-auto">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Chat Messages</h2>
      {chats.length === 0 ? (
        <div className="text-gray-500 text-center py-8">
          No messages yet. Start a conversation!
        </div>
      ) : (
        <div className="space-y-4">
          {chats.map((chat) => (
            <div key={chat.id} className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-medium text-gray-800">{chat.name}</h3>
                  <p className="text-sm text-gray-600">{chat.email}</p>
                </div>
                <span className="text-xs text-gray-500">
                  {chat.timestamp.toLocaleTimeString()}
                </span>
              </div>
                                <p className="text-sm text-gray-700 mb-2">{chat.content}</p>
                  
                  {/* Action inset for assistant messages */}
                  {chat.action && (
                    <div className="bg-gray-50 border-l-4 border-gray-400 p-3 mb-2 rounded-r">
                      <p className="text-xs text-gray-600 font-medium">Action Taken:</p>
                      <p className="text-sm text-gray-800 capitalize">{chat.action.replace('_', ' ')}</p>
                    </div>
                  )}
                  
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {chat.property}
                    </span>
                    {chat.bedrooms && (
                      <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                        {chat.bedrooms} {chat.bedrooms === 1 ? 'Bedroom' : 'Bedrooms'}
                      </span>
                    )}
                    {chat.moveInDate && (
                      <span className="inline-block bg-purple-100 text-purple-800 text-xs px-2 py-1 rounded">
                        Move-in: {new Date(chat.moveInDate).toLocaleDateString()}
                      </span>
                    )}
                  </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ChatDisplay 