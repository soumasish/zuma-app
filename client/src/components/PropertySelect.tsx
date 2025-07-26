import React from 'react'
import type { Community } from '../types'

interface PropertySelectProps {
  value: string
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
  communities: Community[]
}

const PropertySelect: React.FC<PropertySelectProps> = ({ value, onChange, communities }) => {
  return (
    <div className="relative">
      <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
      <select
        id="property"
        name="property"
        value={value}
        onChange={onChange}
        className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        required
      >
        <option value=""></option>
        {communities && communities.length > 0 && communities.map((community) => {
          const humanizedName = community.description.split(' ').slice(0, 2).join(' ')
          return (
            <option key={community.id} value={community.name}>
              {humanizedName}
            </option>
          )
        })}
      </select>
    </div>
  )
}

export default PropertySelect 