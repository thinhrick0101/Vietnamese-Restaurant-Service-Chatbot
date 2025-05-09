import { Tabs } from "expo-router";
import { StyleSheet } from "react-native";
import React from "react";
import { Feather, Ionicons, MaterialIcons } from '@expo/vector-icons';

export default function TabsLayout() {
    return (
        <Tabs
            screenOptions={{
                tabBarActiveTintColor: "#B38B59",
                tabBarInactiveTintColor: "#999",
            }}
        >
            <Tabs.Screen
                name='home'
                options={{
                    headerShown: false,
                    title: 'Home',
                    tabBarIcon: ({ color }) => (
                        <Feather name="home" size={30} color={color} />
                    )
                }}
            />
            <Tabs.Screen
                name='order'
                options={{
                    headerShown: false,
                    title: 'Order',
                    tabBarIcon: ({ color }) => (
                        <MaterialIcons name="shopping-bag" size={30} color={color} />
                    )
                }}
            />
            <Tabs.Screen
                name='chat'
                options={{
                    headerShown: false,
                    title: 'Chat',
                    tabBarIcon: ({ color }) => (
                        <Ionicons name="chatbox-sharp" size={30} color={color} />
                    )
                }}
            />
            
        </Tabs>
    );
}

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
    },
});
