import {fireBaseDB} from "../config/firebase_config";
import {ref, get, set } from "firebase/database";

const Product = ref(fireBaseDB, "products");

const fetchProducts = async (): Promise<Product[]> =>{
    const snapshot = await get(Product);
    const data = snapshot.val();

    const products: Product[] = []
    if (data) {
        for (const key in data) {
            if (data.hasOwnProperty(key)) {
                products.push({...data[key]});
            }
        }
    }
    return products;
}



export {fetchProducts};
    
