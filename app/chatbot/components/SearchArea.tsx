import React from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity } from 'react-native';
import { Ionicons, Feather } from '@expo/vector-icons';

interface SearchAreaProps {
  onLocationSelect?: () => void;
  onSearch?: (text: string) => void;
  onFilterPress?: () => void;
}

const SearchArea: React.FC<SearchAreaProps> = ({ 
  onLocationSelect, 
  onSearch, 
  onFilterPress 
}) => {
    return (
        <View style={styles.container}>
            {/* Location section */}
            <View style={styles.locationContainer}>
                <Text style={styles.locationLabel}>Location</Text>
                <TouchableOpacity 
                  style={styles.locationSelector}
                  onPress={onLocationSelect}
                >
                    <Text style={styles.locationText}>Amsterdam, Netherlands</Text>
                    <Ionicons name="chevron-down" size={20} color="#fff" />
                </TouchableOpacity>
            </View>
            
            {/* Search section */}
            <View style={styles.searchRow}>
                <View style={styles.searchInputContainer}>
                    <Ionicons name="search" size={20} color="#999" style={styles.searchIcon} />
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Pho Ga"
                        placeholderTextColor="#999"
                        onChangeText={onSearch}
                    />
                </View>
                <TouchableOpacity 
                  style={styles.filterButton}
                  onPress={onFilterPress}
                >
                    <Feather name="sliders" size={20} color="#fff" />
                </TouchableOpacity>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        backgroundColor: '#1A1A1A',
        paddingHorizontal: 16,
        paddingTop: 30, 
        paddingBottom: 15, // Reduce this if needed
        borderBottomLeftRadius: 0,
        borderBottomRightRadius: 0,
    },
    locationContainer: {
        marginBottom: 20, // Increased spacing to move content down
        paddingTop: 10, // Added top padding to push content down
    },
    locationLabel: {
        color: '#999',
        fontSize: 14,
        fontFamily: 'Sora-Regular',
        marginBottom: 6, // Increased spacing
    },
    locationSelector: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    locationText: {
        color: '#fff',
        fontSize: 20, // Increased font size to match image
        fontFamily: 'Sora-Medium',
        marginRight: 6,
    },
    searchRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginTop: 8, // Added margin to increase spacing
    },
    searchInputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#2A2A2A',
        borderRadius: 12,
        paddingHorizontal: 12,
        flex: 1,
        marginRight: 10,
        height: 50, // Increased height
    },
    searchIcon: {
        marginRight: 8,
    },
    searchInput: {
        flex: 1,
        color: '#fff',
        fontSize: 16,
        fontFamily: 'Sora-Regular',
        paddingVertical: 12,
    },
    filterButton: {
        backgroundColor: '#D8854E', // Orange color
        width: 50, // Increased size
        height: 50, // Increased size
        borderRadius: 12,
        justifyContent: 'center',
        alignItems: 'center',
    },
});

export default SearchArea;
