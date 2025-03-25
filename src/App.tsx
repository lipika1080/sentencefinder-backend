import { Box, Button, Input, Text } from "@chakra-ui/react";
import { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000"; // Flask API base URL

const App = () => {
  const [sentence, setSentence] = useState("");
  const [vowelCount, setVowelCount] = useState(0);
  const [consonantCount, setConsonantCount] = useState(0);
  const [message, setMessage] = useState("");

  const handleAddSentence = async () => {
    try {
      const response = await axios.post(`${API_BASE}/sentences`, { sentence });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error adding sentence");
    }
  };

  const handleFetchCounts = async () => {
    try {
      const response = await axios.post(`${API_BASE}/sentences/vowels-consonants`, { sentence });
      setVowelCount(response.data.vowels);
      setConsonantCount(response.data.consonants);
    } catch (error) {
      setMessage("Error fetching vowel/consonant count");
    }
  };

  return (
    <Box maxW="500px" mx="auto" mt="50px" textAlign="center">
      <Text fontSize="2xl" mb={4}>Finder App Sentences</Text>
      <Input
        placeholder="Enter a sentence"
        value={sentence}
        onChange={(e) => setSentence(e.target.value)}
        mb={4}
      />
      <Button colorScheme="blue" onClick={handleAddSentence} mr={2}>
        Add Sentence
      </Button>
      <Button colorScheme="green" onClick={handleFetchCounts}>
        Find Vowel & Consonant
      </Button>
      <Text mt={4}>Vowels: {vowelCount}</Text>
      <Text>Consonants: {consonantCount}</Text>
      {message && <Text color="red">{message}</Text>}
    </Box>
  );
};

export default App;
