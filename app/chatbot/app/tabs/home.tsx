import React, { useEffect, useState, useMemo } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, // Make sure StyleSheet is imported
  Image, 
  TouchableOpacity, 
  ScrollView,
  Platform,
  ActivityIndicator
} from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { SafeAreaView } from 'react-native-safe-area-context';
import { FontAwesome } from '@expo/vector-icons';
import { fetchProducts } from '../../services/product';
import { useRouter } from 'expo-router';
import type { Product, ProductCategory } from '../../services/product';
import SearchArea from '../../components/SearchArea';
const router = useRouter();
export default function Home() {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [cart, setCart] = useState<{ [key: string]: number }>({});
    const [error, setError] = useState<string | null>(null);
    const [productCategories, setProductCategories] = useState<ProductCategory[]>([]);
    const [selectedCategory, setSelectedCategory] = useState<string>('All');

    // Function to handle category selection
    const handleCategorySelect = (categoryId: string) => {
        setSelectedCategory(categoryId);

        // Update the selected state of categories
        setProductCategories(prevCategories =>
            prevCategories.map(category => ({
                ...category,
                selected: category.id === categoryId
            }))
        );
    };

    useEffect(() => {
        const loadProducts = async () => {
            try {
                const productsData = await fetchProducts();

                // Extract categories from products and add 'All' option
                const categoryNames = productsData.map(product => product.category);
                const uniqueCategoryNames = Array.from(new Set(categoryNames)).filter(Boolean);

                const categories: ProductCategory[] = [
                    { id: 'All', selected: selectedCategory === 'All' }
                ];

                uniqueCategoryNames.forEach(name => {
                    categories.push({
                        id: name as string,
                        selected: selectedCategory === name
                    });
                });

                setProducts(productsData);
                setProductCategories(categories);
            } catch (err) {
                setError("Error fetching products" + err);
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        loadProducts();
    }, []);

    // Use useMemo to filter products based on selected category
    const filteredProducts = useMemo(() => {
        if (selectedCategory === 'All') {
            return products;
        }
        return products.filter(product => product.category === selectedCategory);
    }, [products, selectedCategory]);

    // Use useMemo to remove duplicates from filtered products
    const uniqueVisibleProducts = useMemo(() => {
        // Additional check in case duplicates still appear
        const seen = new Set();
        return filteredProducts.filter(product => {
            const identifier = product.id || product.name;
            if (seen.has(identifier)) {
                return false;
            }
            seen.add(identifier);
            return true;
        });
    }, [filteredProducts]);

    // Function to add item to cart
    const addToCart = (product: Product) => {
        setCart(prevCart => {
            const productId = product.id || product.name;
            return {
                ...prevCart,
                [productId]: (prevCart[productId] || 0) + 1
            };
        });

        // Optional: Show feedback to user
        console.log(`Added ${product.name} to cart`);
    };

    if (loading) {
        return (
            <SafeAreaView style={styles.loadingContainer}>
                <Text style={styles.loadingText}>Loading...</Text>
            </SafeAreaView>
        );
    }

    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <ScrollView
                style={{ flex: 1 }}
                showsVerticalScrollIndicator={false}
                stickyHeaderIndices={[]}
            >
                <SearchArea
                    onLocationSelect={() => console.log('Location select pressed')}
                    onSearch={(text) => console.log('Searching for:', text)}
                    onFilterPress={() => console.log('Filter button pressed')}
                />

                <SafeAreaView style={styles.container}>
                    <Text style={styles.title}>Vietnamese Specialties</Text>
                    <Text style={styles.subTitle}>
                        {uniqueVisibleProducts.length} items available
                    </Text>

                    {/* Categories */}
                    <View style={styles.categoryScrollContainer}>
                        <ScrollView
                            horizontal
                            showsHorizontalScrollIndicator={false}
                            contentContainerStyle={styles.categoryScroll}
                        >
                            {productCategories.map((category) => (
                                <TouchableOpacity
                                    key={category.id}
                                    style={[
                                        styles.categoryPill,
                                        category.selected ? styles.categoryPillActive : null
                                    ]}
                                    onPress={() => handleCategorySelect(category.id)}
                                >
                                    <Text
                                        style={[
                                            styles.categoryPillText,
                                            category.selected ? styles.categoryPillTextActive : null
                                        ]}
                                    >
                                        {category.id}
                                    </Text>
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    </View>

                    {/* Products grid */}
                    <View style={styles.productsContainer}>
                        {uniqueVisibleProducts.map((item, index) => (
                            <View key={item.id || `${item.name}-${index}`} style={styles.productItem}>
                            <TouchableOpacity
                                style={styles.productTouchable}
                                onPress={() => {
                                    router.push({
                                        pathname: `/tabs/details`,
                                        params: {
                                            name: item.name,
                                            type: item.category,
                                            price: item.price,
                                            description: item.description,
                                            rating: item.rating,
                                        },
                                    });
                                }}
                            >
                                {item.image_url ? (
                                    <Image
                                        style={styles.productImage}
                                        source={{ uri: item.image_url }}
                                    />
                                ) : (
                                    <View style={styles.placeholderImage}>
                                        <Text style={styles.placeholderText}>No Image</Text>
                                    </View>
                                )}
                                <Text 
                                  style={styles.productName} 
                                  numberOfLines={1} 
                                  ellipsizeMode="tail"
                                >
                                  {item.name}
                                </Text>
                                <Text 
                                  style={styles.productCategory} 
                                  numberOfLines={1} 
                                  ellipsizeMode="tail"
                                >
                                  {item.category || "Uncategorized"}
                                </Text>
                                <View style={styles.priceContainer}>
                                    <Text style={styles.productPrice}>
                                        ${item.price?.toFixed(2) || '0.00'}
                                    </Text>
                                    <TouchableOpacity
                                        style={styles.addButton}
                                        onPress={(e) => {
                                            e.stopPropagation(); // Prevent triggering the parent onPress
                                            addToCart(item);
                                        }}
                                        activeOpacity={0.7}
                                    >
                                        <FontAwesome name="plus" size={15} color="#fff" />
                                    </TouchableOpacity>
                                </View>
                            </TouchableOpacity>
                            </View>
                        ))}
                </View>
            </SafeAreaView>
        </ScrollView>
        </GestureHandlerRootView >
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        padding: 5,
        paddingTop: 0, // Remove top padding
    },
    listContainer: {
        padding: 5,
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    loadingText: {
        fontSize: 18,
        fontFamily: 'Sora-Medium',
    },
    title: {
        fontSize: 24,
        fontFamily: 'Sora-Bold',
        marginBottom: 15, // Keep bottom margin
        marginTop: 5, // Reduced top margin
        paddingHorizontal: 5,
    },
    subTitle: {
        fontSize: 14,
        fontFamily: 'Sora-Regular',
        color: '#777',
        marginTop: -10,
        marginBottom: 10,
        paddingHorizontal: 5,
    },
    productItem: {
        width: '48%',  // Exactly 48% of container width
        margin: '1%',  // 1% margin on all sides
        marginBottom: 10, // Add some bottom margin between rows
    },
    productTouchable: {
        backgroundColor: '#fff',
        borderRadius: 10,
        overflow: 'hidden',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 2,
        height: 250, // Fixed height for all cards
    },
    productImage: {
        width: '100%',
        height: 150, // Fixed height for all images
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
        resizeMode: 'cover', // Ensure images cover the space properly
    },
    placeholderImage: {
        width: '100%',
        height: 150, // Match the image height
        backgroundColor: '#e1e1e1',
        justifyContent: 'center',
        alignItems: 'center',
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
    },
    placeholderText: {
        color: '#999',
        fontFamily: 'Sora-Medium',
    },
    productName: {
        fontSize: 16,
        fontFamily: 'Sora-Bold',
        paddingHorizontal: 10,
        paddingTop: 10,
        paddingBottom: 3,
    },
    productCategory: {
        fontSize: 12,
        fontFamily: 'Sora-Regular',
        color: '#888',
        paddingHorizontal: 10,
        marginBottom: 5,
    },
    priceContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 10,
        paddingBottom: 10,
        position: 'absolute', // Position at the bottom
        bottom: 0,
        left: 0,
        right: 0,
    },
    productPrice: {
        fontSize: 16,
        fontFamily: 'Sora-Bold',
        color: '#333',
    },
    addButton: {
        backgroundColor: '#D8854E', // Orange color like in the image
        width: 30,
        height: 30,
        borderRadius: 6,
        justifyContent: 'center',
        alignItems: 'center',
        elevation: 1,
    },
    categoryScrollContainer: {
        width: '100%',
        paddingVertical: 10,
        marginTop: 5,
        marginBottom: 15,
    },
    categoryScroll: {
        paddingHorizontal: 10,
        paddingBottom: 5,
    },
    categoryPill: {
        backgroundColor: '#EDEDED',
        borderRadius: 20,
        paddingVertical: 8,
        paddingHorizontal: 12,
        marginRight: 10,
        justifyContent: 'center',
        alignItems: 'center',
    },
    categoryPillActive: {
        backgroundColor: '#D8854E',
    },
    categoryPillText: {
        fontSize: 14,
        fontFamily: 'Sora-Regular',
        color: '#313131',
    },
    categoryPillTextActive: {
        color: '#fff',
    },
    productsContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
        paddingHorizontal: 5,
        width: '100%',
    },
})