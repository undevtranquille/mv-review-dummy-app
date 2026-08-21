export interface Actor {
    id: number
    first_name: string
    last_name: string
  }
  
  export interface Review {
    id: number
    movie: number
    grade: number
  }
  
  export interface MovieListItem {
    id: number
    title: string
    average_grade: number | null
  }
  
  export interface MovieDetail extends MovieListItem {
    description: string
    actors: Actor[]
    reviews: Review[]
  }