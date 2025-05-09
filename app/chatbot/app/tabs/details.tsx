import { Text, ScrollView } from "react-native-gesture-handler";
import { Image, StyleSheet, View } from "react-native";
import React from "react";
import { useLocalSearchParams } from "expo-router";
import { GestureHandlerRootView } from "react-native-gesture-handler";

const DetailPage = () => {
    const {name, image_url, type, price, description, rating} = useLocalSearchParams() as {
        name: string;
        image_url: string;
        type: string;
        price: string;
        description: string;
        rating: string;
    };

    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <View style={styles.container}>
                <ScrollView contentContainerStyle={styles.scrollContent}>
                    <Text style={styles.title}>{name}</Text>
                    
                    {/* Display image if available */}
                    {image_url && (
                        <Image 
                            source={{ uri: image_url }} 
                            style={styles.image}
                            resizeMode="cover"
                        />
                    )}
                    
                    {/* Product details */}
                    <View style={styles.detailsContainer}>
                        <View style={styles.row}>
                            <Text style={styles.label}>Type:</Text>
                            <Text style={styles.value}>{type}</Text>
                        </View>
                        
                        <View style={styles.row}>
                            <Text style={styles.label}>Price:</Text>
                            <Text style={styles.value}>${parseFloat(price).toFixed(2)}</Text>
                        </View>
                        
                        {rating && (
                            <View style={styles.row}>
                                <Text style={styles.label}>Rating:</Text>
                                <Text style={styles.value}>{rating}/5</Text>
                            </View>
                        )}
                        
                        {description && (
                            <View style={styles.descriptionContainer}>
                                <Text style={styles.descriptionLabel}>Description</Text>
                                <Text style={styles.description}>{description}</Text>
                            </View>
                        )}
                    </View>
                </ScrollView>
            </View>
        </GestureHandlerRootView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    scrollContent: {
        padding: 16,
    },
    title: {
        fontSize: 24,
        fontFamily: 'Sora-Bold',
        marginBottom: 20,
        color: '#333',
    },
    image: {
        width: '100%',
        height: 250,
        borderRadius: 16,
        marginBottom: 24,
    },
    detailsContainer: {
        backgroundColor: '#f9f9f9',
        borderRadius: 16,
        padding: 20,
        marginBottom: 24,
    },
    row: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 12,
    },
    label: {
        fontSize: 16,
        fontFamily: 'Sora-Medium',
        color: '#666',
        width: 80,
    },
    value: {
        fontSize: 16,
        fontFamily: 'Sora-Regular',
        color: '#333',
        flex: 1,
    },
    descriptionContainer: {
        marginTop: 8,
    },
    descriptionLabel: {
        fontSize: 18,
        fontFamily: 'Sora-Medium',
        color: '#333',
        marginBottom: 8,
    },
    description: {
        fontSize: 15,
        fontFamily: 'Sora-Regular',
        color: '#555',
        lineHeight: 22,
    }
});

export default DetailPage;
