export interface ChatMessage {
  id: string
  name: string
  email: string
  content: string
  property: string
  bedrooms?: number
  moveInDate?: string
  action?: string
  timestamp: Date
}

export interface FormData {
  name: string
  email: string
  content: string
  property: string
  bedrooms: number
  moveInDate: string
}

export interface Community {
  id: number
  name: string
  description: string
}

export interface ReplyRequest {
  lead: {
    name: string
    email: string
  }
  message: string
  preferences: {
    bedrooms: number
    move_in: string
  }
  community_id: string
}

export interface ReplyResponse {
  reply?: string
  message?: string
  action: string
  proposed_time?: string | null
  missing_info?: string
} 