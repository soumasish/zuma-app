import React from 'react'

interface DatePickerProps {
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
}

const DatePicker: React.FC<DatePickerProps> = ({ value, onChange }) => {
  return (
    <div className="relative">
      <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
              <input
          type="date"
          id="moveInDate"
          name="moveInDate"
          value={value}
          onChange={onChange}
          className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder=""
          required
        />
    </div>
  )
}

export default DatePicker 