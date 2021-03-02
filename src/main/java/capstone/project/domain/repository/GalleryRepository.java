package capstone.project.domain.repository;

import capstone.project.domain.entity.GalleryEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface GalleryRepository extends JpaRepository<GalleryEntity, Long> {
}