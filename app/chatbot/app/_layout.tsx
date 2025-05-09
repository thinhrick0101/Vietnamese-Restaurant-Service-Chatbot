// <reference types="nativewind/types" />
import { Stack } from 'expo-router';
import { LogBox } from 'react-native';
import { useFonts } from 'expo-font';
import { useEffect } from 'react';
import * as SplashScreen from 'expo-splash-screen';

// Keep the splash screen visible while fonts load
SplashScreen.preventAutoHideAsync();

// Suppress warnings
LogBox.ignoreLogs([
  'Non-serializable values were found in the navigation state',
]);

// Make sure to export a component as the default export
export default function Layout() {
  const [fontsLoaded] = useFonts({
    "Sora-Regular": require('../assets/fonts/Sora-Regular.ttf'),
    "Sora-Bold": require('../assets/fonts/Sora-Bold.ttf'),
    "Sora-SemiBold": require('../assets/fonts/Sora-SemiBold.ttf'),
    "Sora-Medium": require('../assets/fonts/Sora-Medium.ttf'),
    "Sora-Light": require('../assets/fonts/Sora-Light.ttf'),
    "Sora-ExtraLight": require('../assets/fonts/Sora-ExtraLight.ttf'),
    "Sora-Thin": require('../assets/fonts/Sora-Thin.ttf'),
  });

  useEffect(() => {
    // Hide splash screen when fonts are loaded
    if (fontsLoaded) {
      SplashScreen.hideAsync();
    }
  }, [fontsLoaded]);

  // Don't render anything until fonts are loaded
  if (!fontsLoaded) {
    return null;
  }

  return (
    <Stack>
      <Stack.Screen name="index" options={{ headerShown: false }} />
      <Stack.Screen name="tabs" options={{ headerShown: false }} />
      <Stack.Screen name="details" options={{ headerShown: false }} />
    </Stack>
  );
}