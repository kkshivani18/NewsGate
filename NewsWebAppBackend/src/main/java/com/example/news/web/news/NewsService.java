package com.example.news.web.news;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class NewsService {

    @Value("${news.api.url}")
    private String newsApiUrl; // URL of the News API

    @Value("${news.api.key}")
    private String apiKey; // API key for the News API

    public final RestTemplate restTemplate;

    public NewsService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // Fetch news for admin role
    public String getAdminNews() {
        String url = String.format("%s?country=us&apiKey=%s", newsApiUrl, apiKey);
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }

    // Fetch news for premium users
    public String getPremiumNews() {
        // displaying that premium user has used filter to get specific news (By choice)
        String url = String.format("%s?country=us&category=business&apiKey=%s", newsApiUrl, apiKey);
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }

    // Fetch news for general users
    public String getGeneralNews() {
        // In general content is displayed.
        String url = String.format("%s?country=us&category=general&apiKey=%s", newsApiUrl, apiKey);
        ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
        return response.getBody();
    }
}