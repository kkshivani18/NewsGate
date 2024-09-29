package com.example.news.web.news;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/news")
public class NewsController {

    private final NewsService newsService;

    public NewsController(NewsService newsService) {
        this.newsService = newsService;
    }

    @GetMapping("/admin")
    @PreAuthorize("hasRole('ROLE_ADMIN')")
    public String getAdminNews() {
        return newsService.getAdminNews();
    }

    @GetMapping("/premium")
    @PreAuthorize("hasRole('ROLE_PREMIUM')")
    public String getPremiumNews() {
        return newsService.getPremiumNews();
    }

    @GetMapping("/user")
    @PreAuthorize("hasRole('ROLE_USER')")
    public String getGeneralNews() {
        return newsService.getGeneralNews();
    }
}
