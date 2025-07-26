import React from 'react'

interface BedroomsSelectProps {
  value: number
  onChange: (e: React.ChangeEvent<HTMLSelectElement>) => void
}

const BedroomsSelect: React.FC<BedroomsSelectProps> = ({ value, onChange }) => {
  const bedrooms = [1, 2, 3, 4, 5]

  return (
    <div className="relative">
      <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5a2 2 0 012-2h4a2 2 0 012 2v2H8V5z" />
        </svg>
      </div>
      <select
        id="bedrooms"
        name="bedrooms"
        value={value}
        onChange={onChange}
        className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        required
      >
        <option value=""></option>
        {bedrooms.map((bedroom) => (
          <option key={bedroom} value={bedroom}>
            {bedroom}
          </option>
        ))}
      </select>
    </div>
  )
}

export default BedroomsSelect 