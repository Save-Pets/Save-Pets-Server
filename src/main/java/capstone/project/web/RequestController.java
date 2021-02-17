package capstone.project.web;


import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class RequestController {

    @GetMapping("/picture/1")
    void getImage(){

    }

}
