package capstone.project.web.dto;

import capstone.project.domain.Posts.Posts;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Getter
@ToString
@NoArgsConstructor
//프론트 단에서 받아오는 데이터들 (임의 값: 여기선 간단하게 id 와 filePath)
public class PostsDto {
    private Long id;
    private String filePath;

    @Builder
    public PostsDto(Long id, String filePath){
        this.id=id;
        this.filePath=filePath;
    }

    public Posts toEntity(){
        return Posts.builder()
                .id(id)
                .filePath(filePath)
                .build();
    }


}
