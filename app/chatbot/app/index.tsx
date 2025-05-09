import { ImageBackground } from "expo-image";
import { Text, View, StyleSheet, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { LinearGradient } from 'expo-linear-gradient';
import { useFonts } from 'expo-font';
import { router } from "expo-router";

export default function Index() {
  const [fontsLoaded] = useFonts({
    "Sora-Medium": require('../assets/fonts/Sora-Medium.ttf'),
    "Sora-Bold": require('../assets/fonts/Sora-Bold.ttf'),
    "Sora-Regular": require('../assets/fonts/Sora-Regular.ttf'),
    "Vollkorn-Regular": require('../assets/fonts/Vollkorn-Regular.ttf'),
    "Vollkorn-Bold": require('../assets/fonts/Vollkorn-Bold.ttf'),
    "Vollkorn-SemiBold": require('../assets/fonts/Vollkorn-SemiBold.ttf'),
  });

  if (!fontsLoaded) {
    return null; // or a loading indicator
  }

  const handleStart = () => {
    // Navigate to your main screen
    router.push({ pathname: "/tabs/home" });
  };

  return (
    <View style={styles.container}>
      <SafeAreaView style={styles.safeArea}>
        <ImageBackground
          style={styles.backgroundImage}
          source={require("../assets/images/onboarding.png")}
          contentFit="cover"
        >
          {/* Top content */}
          <View style={styles.contentContainer}>
            <LinearGradient
              colors={['rgba(0, 0, 0, 0.25)', 'transparent']}
              style={styles.textBackground}
            >
              <Text style={styles.preTitle}>Savor the Flavor of</Text>
              <Text style={styles.title}>Vietnamese</Text>
              <Text style={styles.subtitle}>Order Your Favorite Vietnamese Dishes.</Text>
            </LinearGradient>
          </View>
          
          {/* Bottom button container */}
          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={styles.startButton}
              onPress={handleStart}
              activeOpacity={0.8}
            >
              <LinearGradient
                colors={['#B38B59', '#F5DEB3']}
                style={styles.buttonGradient}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
              >
                <Text style={styles.buttonText}>Get Started</Text>
              </LinearGradient>
            </TouchableOpacity>
          </View>
        </ImageBackground>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  backgroundImage: {
    flex: 1,
    width: '100%',
    justifyContent: 'space-between', // This spreads children to top and bottom
  },
  contentContainer: {
    width: '100%',
    paddingTop: '15%',
    alignItems: 'center',
  },
  textBackground: {
    padding: 20,
    borderRadius: 10,
    width: '90%',
    alignItems: 'center',
  },
  preTitle: {
    color: '#F5DEB3',
    fontSize: 20,
    fontFamily: 'Vollkorn-Regular',
    textAlign: 'center',
  },
  title: {
    color: '#F5DEB3',
    fontSize: 42,
    fontFamily: 'Vollkorn-Bold',
    textAlign: 'center',
    marginVertical: 8,
  },
  subtitle: {
    color: '#F5DEB3',
    fontSize: 16,
    fontFamily: 'Sora-Regular',
    textAlign: 'center',
  },
  buttonContainer: {
    width: '100%',
    paddingBottom: 40, // Adjust this to position the button from the bottom
    alignItems: 'center',
  },
  startButton: {
    width: '80%',
    height: 56,
    borderRadius: 28,
    overflow: 'hidden',
    elevation: 5, // Android shadow
    shadowColor: '#000', // iOS shadow
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  buttonGradient: {
    width: '100%',
    height: '100%',
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonText: {
    color: '#3A2D1C',
    fontSize: 18,
    fontFamily: 'Sora-Bold',
    textAlign: 'center',
  }
});
