package capstone.project.service;

import capstone.project.domain.repository.GalleryRepository;
import capstone.project.dto.GalleryDto;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@AllArgsConstructor
public class GalleryService {
    private GalleryRepository galleryRepository;

    public void savePost(GalleryDto galleryDto) {
        galleryRepository.save(galleryDto.toEntity());
    }
}
