export interface Product {
    id: string;
    name: string;
    description: string;
    price: number;
    image: string;
    rating: number;
    reviews: number;
    category: string;
  } 

export interface ProductCategory {
    id: string;
    selected: boolean;
  }