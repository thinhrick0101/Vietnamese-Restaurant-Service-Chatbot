import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const Banner = () => {
  return (
    <TouchableOpacity style={styles.container} activeOpacity={0.95}>
      <Image 
        source={require('../assets/images/banner.png')}
        style={styles.bannerImage}
        resizeMode="cover"
      />
      <LinearGradient
        colors={['rgba(0,0,0,0.1)', 'rgba(0,0,0,0.6)']}
        style={styles.gradient}
      >
        <View style={styles.textContainer}>
          <Text style={styles.bannerTitle}>Authentic Vietnamese Cuisine</Text>
          <Text style={styles.bannerSubtitle}>Experience traditional flavors</Text>
          <TouchableOpacity style={styles.orderButton}>
            <Text style={styles.orderButtonText}>Order Now</Text>
          </TouchableOpacity>
        </View>
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    height: 180,
    borderRadius: 12,
    overflow: 'hidden',
    marginHorizontal: 10,
    marginVertical: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  bannerImage: {
    width: '100%',
    height: '100%',
    position: 'absolute',
  },
  gradient: {
    flex: 1,
    justifyContent: 'flex-end',
    padding: 15,
  },
  textContainer: {
    maxWidth: '80%',
  },
  bannerTitle: {
    color: '#FFFFFF',
    fontSize: 22,
    fontFamily: 'Sora-Bold',
    marginBottom: 5,
    textShadowColor: 'rgba(0, 0, 0, 0.75)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  bannerSubtitle: {
    color: '#FFFFFF',
    fontSize: 14,
    fontFamily: 'Sora-Regular',
    marginBottom: 12,
    opacity: 0.9,
    textShadowColor: 'rgba(0, 0, 0, 0.5)',
    textShadowOffset: { width: 0, height: 1 },
    textShadowRadius: 2,
  },
  orderButton: {
    backgroundColor: '#D8854E',
    paddingVertical: 8,
    paddingHorizontal: 15,
    borderRadius: 8,
    alignSelf: 'flex-start',
    marginBottom: 5,
  },
  orderButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontFamily: 'Sora-Medium',
  }
});

export default Banner;