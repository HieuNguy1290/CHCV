// Vietnamese translations of the guide content in game_guides.dart.

typedef VietnameseGameGuide = ({
  String objective,
  String controls,
  List<String> walkthrough,
  List<String> strategies,
});

const vietnameseGameGuides = <String, VietnameseGameGuide>{
  "vector_dot_product": (
    objective: "Tính tích vô hướng của hai vectơ 2D bằng công thức u · v = u_x × v_x + u_y × v_y.",
    controls: "Chọn đáp án bằng tích vô hướng của hai vectơ.",
    walkthrough: [
      "Nhân hai thành phần theo trục X.",
      "Nhân hai thành phần theo trục Y.",
      "Cộng hai tích rồi chọn đáp án.",
    ],
    strategies: [
      "Kiểm tra dấu âm. Ví dụ, (−2) × 3 = −6.",
      "Hai vectơ vuông góc có tích vô hướng bằng 0.",
    ],
  ),
  "stroop_number_size": (
    objective: "Chọn nhanh số lớn hơn theo yêu cầu trên màn hình: so sánh giá trị số hoặc kích thước chữ.",
    controls: "Bấm nút bên trái hoặc bên phải.",
    walkthrough: [
      "Đọc yêu cầu xem lượt này so sánh giá trị hay kích thước chữ.",
      "Bỏ qua yếu tố còn lại. Ví dụ, khi so sánh giá trị thì bỏ qua cỡ chữ.",
      "Bấm nút ở bên có đáp án đúng.",
    ],
    strategies: [
      "Đọc yêu cầu trước khi nhìn hai số.",
      "Cẩn thận khi số 9 in nhỏ còn số 2 in lớn.",
    ],
  ),
  "word_ladder_step": (
    objective: "Tìm từ trung gian giữa từ đầu và từ cuối sao cho mỗi bước chỉ đổi một chữ cái.",
    controls: "Chọn từ trung gian hợp lệ trong các đáp án.",
    walkthrough: [
      "So sánh từ đầu với từ cuối để tìm các chữ cái khác nhau.",
      "Tìm một từ chỉ khác mỗi đầu đúng một chữ cái.",
      "Chọn từ trung gian phù hợp.",
    ],
    strategies: [
      "Từ trung gian phải là một từ tiếng Anh hợp lệ.",
      "Kiểm tra vị trí từng chữ cái được thay.",
    ],
  ),
  "corsi_backward_span": (
    objective: "Quan sát một chuỗi khối không gian nhấp nháy và đập các khối theo thứ tự ngược lại chính xác (từ phía sau).",
    controls: "Mở các khối không gian trên màn hình theo trình tự ngược lại.",
    walkthrough: [
      "Xem các khối được chiếu sáng theo thứ tự đi lại.",
      "Một cách tinh thần đảo ngược quỹ đạo tự do.",
      "Gõ các khối từ khối cuối cùng được chiếu sáng trở lại khối đầu tiên.",
    ],
    strategies: [
      "Khóa khối cuối cùng được chiếu sáng mạnh mẽ trong bộ nhớ hình ảnh như điểm khởi đầu của bạn.",
      "Lần theo đường không gian ngược lại trên bảng.",
    ],
  ),
  "ab_reversal_oddball": (
    objective: "Đáp ứng mục tiêu kích thích và chuyển đổi các quy tắc phản ứng ngay khi mục tiêu đảo ngược.",
    controls: "Tap TARGEt hoặc NON-EPET.",
    walkthrough: [
      "Kiểm tra băng cờ quy tắc mục tiêu ở trên cùng.",
      "Quan sát hình ảnh được trình bày (square vs Circle).",
      "Nhấn TARGET nếu nó khớp với quy tắc hiện tại, còn lại là NON-FET.",
    ],
    strategies: [
      "Hãy cảnh giác với luật thay đổi thông báo.",
      "Điều khiển phản xạ động cơ trước đây ngay khi quy tắc thay đổi.",
    ],
  ),
  "conundrum_anagram": (
    objective: "Giải mã tất cả 9 chữ cái thành một từ tiếng Anh hợp lệ.",
    controls: "Chữ cái gõ để đánh vần chữ, gõ lại để hoàn tác.",
    walkthrough: [
      "Kiểm tra hồ bơi 9 chữ cái.",
      "Tìm kiếm các tiền tố chung (DIS-, UN-) và hậu tố (ING, rection, hits).",
      "Đánh vần từ 9 chữ cái đầy đủ.",
    ],
    strategies: [
      "Các nhóm phụ âm với các âm thanh giống nhau.",
      "Hãy thử xây dựng kết thúc trước tiên để khám phá gốc rễ.",
    ],
  ),
  "binary_matrix_rank": (
    objective: "Xác định cấp đại số tuyến tính (1, 2, hoặc 3) của ma trận nhị phân 3x3 theo mô-đun 2.",
    controls: "Tap RANK 1, RANK 2, hay RANK 3.",
    walkthrough: [
      "Xem xét các dòng véc- tơ của ma trận nhị phân 3 x 3.",
      "Kiểm tra các hàng hoặc hàng giống hệt nhau được hình thành bởi tổng cộng XOR của hai hàng khác.",
      "Gõ vào cấp độ tương ứng.",
    ],
    strategies: [
      "Nếu cả ba hàng là riêng biệt và không có hàng là tổng của XOR khác, cấp là 3.",
      "Nếu hai hàng giống hệt nhau hoặc tất cả các hàng là nhiều, cấp là 1 hoặc 2.",
    ],
  ),
  "visual_crowding_acuity": (
    objective: "Xóa bỏ sự định hướng của vành đai trung tâm Landolt trước sự hiện diện của vành đai đánh lạc hướng.",
    controls: "Đánh vào mũi tên hướng tương ứng với hướng khoảng trống trung tâm (UP, down, left, right).",
    walkthrough: [
      "Tập trung toàn bộ sự chú ý vào vòng giữa Landolt.",
      "lọc ra sự can thiệp từ các vòng cạnh bên.",
      "Gõ vào hướng mũi tên tương ứng.",
    ],
    strategies: [
      "Thu hẹp sự chú ý của anh vào ranh giới vòng trung tâm.",
      "Đừng nhìn vào sườn bên ngoài, hãy xác định vết nứt ở vòng chính.",
    ],
  ),
  "probe_digit_span": (
    objective: "Hãy quan sát một dòng chữ số ngẫu nhiên nhanh chóng và nhớ lại con số mà ngay sau con số thăm dò.",
    controls: "Đạp số trên bàn phím màn hình.",
    walkthrough: [
      "Hãy chú ý đến con số nhỏ.",
      "Khi có số máy thăm dò, hãy kiểm tra bộ nhớ ngắn hạn của bạn để tìm người kế nhiệm ngay lập tức.",
      "Hãy nhập số vào numpad.",
    ],
    strategies: [
      "Mật mã chữ số theo cặp nhanh (ví dụ '3-8', '5-2' để nhanh chóng nhớ lại liên kết kế nhiệm.",
      "Duy trì một vòng âm thanh trong bộ nhớ hoạt động.",
    ],
  ),
  "pythagorean_triple_builder": (
    objective: "Tính toán chiều dài bên bị thiếu theo số lượng tam giác bên phải bằng a2 + b2 = c2.",
    controls: "Gõ chính xác giá trị số nguyên thiếu từ các tùy chọn.",
    walkthrough: [
      "Nhận diện chân cho (a, b) và Pitago (c).",
      "Áp dụng công thức Pythagorean: c = c(a2 + b2) hoặc a = c2 - b2).",
      "Chọn kết quả số nguyên khớp.",
    ],
    strategies: [
      "Hãy nhớ lại ba phần nguyên thủy phổ biến như (3, 4, 5), (5, 12, 13), (8, 15, 17).",
      "Nhiều bộ ba (ví dụ 6, 8, 10).",
    ],
  ),
  "visual_search_conjunction": (
    objective: "Xác định xem hình của mục tiêu (hình vuông đỏ) có mặt giữa các bộ phân tích màu/shape.",
    controls: "Báo cáo tình hình hoặc sở khởi.",
    walkthrough: [
      "Ghi nhớ cả hai kích thước tính năng (Red + Square).",
      "Quét nhanh màn hình cho tổ hợp độc nhất vô nhị.",
      "Báo động báo nếu tìm thấy Quảng trường Đỏ, nếu không hãy báo cáo ABSENT.",
    ],
    strategies: [
      "Bộ lọc phân cách màu trước (chỉ có thể các mục màu đỏ cho các đường viền vuông).",
      "Quét theo các rãnh ngang có cấu trúc bên ngoài màn hình.",
    ],
  ),
  "wireframe_3d_rotation": (
    objective: "Xác định chính xác khung dây 3D được xoay sau khi quay trục Yaw.",
    controls: "Hãy gõ vào tùy chọn khung dây xoay.",
    walkthrough: [
      "Theo dõi định hướng dây ba chiều ban đầu.",
      "tâm trí quay mô hình xung quanh trục Y theo độ đã chỉ định.",
      "Gõ tùy chọn này cho thấy quan điểm tương ứng.",
    ],
    strategies: [
      "Theo dõi đỉnh đầu tiên hoặc đỉnh cao trong quá trình quay.",
      "Loại bỏ các tùy chọn khi cạnh cơ bản đảo chiều sâu không đúng.",
    ],
  ),
  "word_pair_associate_memory": (
    objective: "Việc học hỏi kết hợp các mối quan hệ và chọn chính xác từ bạn bè khi được nhắc đến với một dấu hiệu.",
    controls: "Gõ vào từ khớp với mục tiêu giữa các lựa chọn.",
    walkthrough: [
      "Ghi nhớ cặp trong quá trình đếm ngược (ví dụ 'DOCTOR - HOPITAL').",
      "Khi được trình bày với \"DOCTOR\", xác định vị trí \"HOPTAL\".",
      "Nhấn nút lựa chọn đúng.",
    ],
    strategies: [
      "Tạo ra sự kết nối sống động giữa các khái niệm đôi.",
      "Hãy xem lại từng cặp một trong giai đoạn học hỏi.",
    ],
  ),
  "hitori": (
    objective: "Che mờ số trùng trong lưới để không có hàng hay cột chứa lặp lại giữa các tế bào chưa được che mờ, các ô màu đen không chạm vào hay không chạm vào, và các tế bào chưa bóng vẫn còn được kết nối.",
    controls: "Gõ một xà lim một lần để bóng mát (đen), gõ hai lần để vòng tròn (an toàn).",
    walkthrough: [
      "Xác định hàng và cột với số trùng.",
      "Bóng râm sao cho chỉ có thể nhìn thấy được một lần.",
      "Các tế bào có bóng râm không bao giờ gần hoặc không bao giờ cạnh nhau.",
    ],
    strategies: [
      "Nếu một tế bào được tô màu đen, tất cả bốn tế bào lân cận phải được tháo bóng (thô tròn chúng).",
      "Giữa hai số giống hệt nhau với một tế bào ở giữa, tế bào giữa phải được bỏ bóng.",
    ],
  ),
  "modular_clock_arithmetic": (
    objective: "Tính toán thời gian chu kỳ theo số học theo mô-đun 12 theo mô-đun.",
    controls: "Ấn nút tương ứng với giờ tới.",
    walkthrough: [
      "Kiểm tra giờ bắt đầu trên đồng hồ tương tự.",
      "Thêm số giờ cho trước và giảm qui mô 12.",
      "Nhấn nút đồng hồ đi.",
    ],
    strategies: [
      "Cứ mỗi 12 hay 24 giờ lại quay về đúng vị trí đó.",
      "Trừ đi số lượng lớn nhất của 12 đầu tiên để tính nhanh chóng.",
    ],
  ),
  "temporal_order_judgment": (
    objective: "Trước hết, quan xét nào trong hai vòng tròn ngoại vi ngắn sẽ xảy ra.",
    controls: "Gõ trước hoặc rẽ phải trước.",
    walkthrough: [
      "Tập trung vào giữa '+' crosshai.",
      "Quan sát hai vòng tròn nhấp nháy nhanh chóng.",
      "Chọn bên nào được phóng sáng trước.",
    ],
    strategies: [
      "Đừng theo dõi mắt sang một bên, hãy giữ cái nhìn trung tâm của bạn cố định.",
      "Hãy tin tưởng trực giác của bạn ngay lập tức.",
    ],
  ),
  "polyomino_tiling": (
    objective: "Sắp xếp và xoay các mảnh tetromino để gạch toàn bộ bảng 4x4 mà không cần chồng lên nhau.",
    controls: "Đập một mảnh để chọn, đập ROTATE, sau đó chạm vào một tế bào mạng lưới để đặt.",
    walkthrough: [
      "Chọn một miếng trong khay.",
      "Xoay nếu cần thiết để vừa khít với không gian bảng rỗng.",
      "Nhấn ga để đặt nó.",
    ],
    strategies: [
      "Đặt những mảnh vụng về (như hình L và J) trước.",
      "Để lại những lỗ hổng thân thiện cho mảnh O.",
    ],
  ),
  "yajilin": (
    objective: "Vẽ một vòng khép kín thông qua các tế bào không có bóng và các tế bào màu đen theo đầu mũi tên chỉ hướng đếm mà không có các tế bào màu đen kế bên.",
    controls: "Tế bào đập để vẽ các đoạn lặp; gõ đôi để bật/tắt đen.",
    walkthrough: [
      "Kiểm tra các đầu mối mũi tên chỉ ra chính xác số hồng cầu theo hướng đó.",
      "bảo đảm không có hai tế bào đen nào chạm vào hoặc không chạm vào.",
      "Vẽ một vòng tròn liên tục thăm viếng tất cả các bạch cầu còn lại.",
    ],
    strategies: [
      "Không thể thăm viếng các tế bào gợi ý bởi vòng lặp và không thể bị bóng đen bao phủ.",
      "Nếu một tế bào được tô màu đen, vòng thời gian phải đi vòng quanh nó.",
    ],
  ),
  "algebraic_inequality_solver": (
    objective: "Cô lập nhanh chóng các biến số và giải quyết các bước một chiều tuyến tính và hai bước khác nhau.",
    controls: "Hãy gõ vào biểu hiện bất bình đẳng chính xác từ các lựa chọn.",
    walkthrough: [
      "Xem xét biểu thức đại số (ví dụ 3x + 5 < 17).",
      "trừ đi các số hạng hằng số và chia cho hệ số của x.",
      "Chọn giải pháp tương ứng (ví dụ x < 4).",
    ],
    strategies: [
      "Thực hiện thứ tự thao tác đảo ngược (subtract/add/add trước, sau đó chia/ phân chia).",
      "Theo dõi hướng bất bình đẳng.",
    ],
  ),
  "attentional_blink_probe": (
    objective: "Phát hiện cho dù một chữ cái thăm dò thứ hai ('X') xuất hiện nhanh chóng trình diễn hình ảnh sau khi mục tiêu chính.",
    controls: "Có hoặc không sau khi dòng suối kết thúc.",
    walkthrough: [
      "Tập trung vào dòng dao cắt nhanh các mục số.",
      "Xác định mục tiêu chính (từ xanh) và tìm một dấu 'X' tiếp theo.",
      "Báo cáo xem chữ X có xuất hiện ở dòng suối không.",
    ],
    strategies: [
      "Tránh chú tâm vào mục tiêu đầu tiên để bộ đệm thị giác của bạn được mở lại nhanh chóng.",
      "Giữ cho mắt tập trung bình tĩnh.",
    ],
  ),
  "masyu": (
    objective: "Vẽ một vòng không tương tác đi qua mỗi vòng tròn, đi thẳng qua các vòng tròn trắng và chuyển qua các tế bào kế nhau; xoay 90° trên các vòng tròn đen và đi thẳng qua các tế bào lân cận.",
    controls: "Tap và kéo hoặc tap chấm kề nhau để vẽ/erase vòng thời gian đoạn.",
    walkthrough: [
      "Kiểm tra vị trí của ngọc trai; ngọc trai trắng yêu cầu xuyên qua, ngọc trai đen yêu cầu một góc 90°.",
      "Kết nối các nút nối với nhau bằng cách gõ để xây dựng đường dẫn.",
      "Đóng vòng thời gian lại mà không có nhánh hoặc ngõ cụt.",
    ],
    strategies: [
      "Ngọc trai đen ở gần mép phải quay bên trong.",
      "Ngọc trai trắng dọc theo bức tường phải đi song song với biên giới.",
    ],
  ),
  "prime_gap_hunt": (
    objective: "Tính toán chính xác sự khác biệt giữa hai số nguyên tố liên tiếp.",
    controls: "Gõ đúng nút thoát hiểm chính xác.",
    walkthrough: [
      "Xem xét hai số nguyên tố liên tiếp được hiển thị trên các quân bài.",
      "Trừ đi nguyên tố nhỏ hơn từ số nguyên tố lớn hơn.",
      "Chọn sự khác biệt số tương ứng trong lưới.",
    ],
    strategies: [
      "Số nguyên tố đôi luôn có khoảng cách 2 (ví dụ 11 & 13, 17 & 19, 41 & 43).",
      "Số nguyên tố anh em họ có một khoảng cách là 4, và số nguyên tố gợi cảm có khoảng cách là 6.",
    ],
  ),
  "heyawake": (
    objective: "Tế bào sơn đen hoặc trắng trong các phòng hình chữ nhật theo các hạn chế phòng số.",
    controls: "Gõ vào một phòng trống một lần để sơn đen, gõ hai lần để đánh dấu chấm xanh lá cây.",
    walkthrough: [
      "Kiểm tra các phòng có số; mỗi phòng xác định chính xác số các hồng cầu bên trong căn phòng đó.",
      "bảo đảm không có hai tế bào đen nào chạm vào hoặc không chạm vào.",
      "Giữ cho tất cả các tế bào bạch cầu chưa được che mờ kết nối với nhau theo một con đường mở.",
    ],
    strategies: [
      "Một căn phòng với số 0 phải có tất cả bạch cầu.",
      "Hành lang trắng không thể băng qua hơn hai phòng liên tiếp trên một đường thẳng.",
    ],
  ),
  "set_theory_venn": (
    objective: "Chọn những vùng chính xác của biểu đồ Venn phù hợp với công thức lý thuyết thiết lập.",
    controls: "Các vùng của sơ đồ Venn hoặc không gian bên ngoài để chọn chúng, sau đó gõ SUBMIT.",
    walkthrough: [
      "Đọc biểu thức tập hợp (e.g., A_B, A_ A-B, A-B, (A-A- B).",
      "Xác định mục tiêu công thức chỉ là A, chỉ B, giao lộ, hay vũ trụ bên ngoài.",
      "Bật tắt thẻ vùng thích hợp và gửi câu trả lời.",
    ],
    strategies: [
      "Giao cắt (Grain) chỉ có nghĩa là vùng chồng chéo.",
      "Liên đoàn kết hợp tất cả các phần nội thất của cả hai bộ phận.",
      "Lời khen () ám chỉ tất cả mọi thứ bên ngoài bộ đã xác định.",
    ],
  ),
  "navon_hierarchical": (
    objective: "Xác định mức độ chữ cái đã yêu cầu (từ lớn vô định chống lại chữ cái nhỏ của địa phương) dưới sự thay đổi nhanh chóng của quy tắc.",
    controls: "Hãy nhấn nút khớp chữ cái từ các lựa chọn.",
    walkthrough: [
      "Hãy kiểm tra quy tắc nhắc nhở: Toàn cục (hình trên bảng) hay địa phương (các yếu tố nhỏ).",
      "Kiểm tra con số tổng hợp.",
      "Gõ vào lá thư tương ứng với chỉ dẫn nhanh.",
    ],
    strategies: [
      "Đừng nhìn vào toàn bộ chữ nếu yêu cầu cục bộ; hãy phóng to thành một ký tự điểm ảnh.",
      "Tập trung đôi mắt của bạn một chút để ngay lập tức nhận thức hình dạng toàn cầu.",
    ],
  ),
  "tapa": (
    objective: "Vẽ một bức tường đen liên tục đến nỗi tất cả những con số gợi ý cho thấy những khối tường liên tục xung quanh mỗi tế bào, không có 2x2 hình vuông đen.",
    controls: "Gõ vào một xà lim trống một lần để đánh dấu như là tường, gõ hai lần để đánh dấu với một chấm đỏ.",
    walkthrough: [
      "Kiểm tra số tế bào; mỗi con số cho thấy chiều dài của những khối được tô bóng liên tiếp xung quanh nó.",
      "Kiểm tra tất cả các ô đen hình thành một mạng kết nối duy nhất.",
      "Không bao giờ cho phép khối 2x2 rắn của các tế bào màu đen.",
    ],
    strategies: [
      "Tế bào manh mối không bao giờ có thể được tô đen.",
      "Một tế bào với '8' phải được bao quanh bởi 8 tế bào đen.",
      "Những khối chồng chéo nhau được tách ra bởi những không gian không có bóng làm thành nhiều số đầu mối như (1, 1) hay (1, 2).",
    ],
  ),
  "exponent_tower": (
    objective: "Tính toán quyền lực và xếp các biểu thức cấp số nhân theo thứ tự tăng từ nhỏ nhất đến lớn nhất.",
    controls: "Bạn có thể đập những khối năng lượng có sẵn để thêm chúng vào tháp của bạn; những cái vòi đặt những khối để loại bỏ chúng.",
    walkthrough: [
      "Tính giá trị số của mỗi cơ số được nâng lên lũy thừa.",
      "Nhấn nguồn năng lượng nhỏ nhất trước để tạo thành chân tháp.",
      "Sắp xếp các quyền lực lên trên theo thứ tự số học nghiêm ngặt.",
    ],
    strategies: [
      "Hãy nhớ sức mạnh chính của 2 (ví dụ 2^5 = 32, 2^ 6 = 64) và 3(3^ 3 = 27, 3^ 4 = 81).",
      "So sánh cùng một cơ sở với số mũ trực tiếp.",
    ],
  ),
  "posner_spatial_cueing": (
    objective: "Phản ứng nhanh và chính xác nhất có thể khi mục tiêu xuất hiện bên trái hoặc bên phải màn hình.",
    controls: "Tháp rời hoặc nút bên phải phù hợp với vị trí mục tiêu.",
    walkthrough: [
      "Giữ trọng tâm của bạn khóa vào dấu thập '+' trung tâm.",
      "Xin lưu ý dấu hiệu đánh dấu trong hộp chớp (động tác: dấu hiệu đôi khi là kẻ đánh lạc hướng không hợp lệ).",
      "Khi vòng tròn đích xuất hiện, tức khắc nhấn vào nút bên tương ứng.",
    ],
    strategies: [
      "Không đoán trước khi vòng tròn đích thực sự thực hiện.",
      "Giữ cái nhìn trung tâm cố định trong thời gian phản ứng ngoại biên nhanh nhất.",
    ],
  ),
  "gear_train_direction": (
    objective: "Xác định nếu mục tiêu '?' thiết bị sẽ xoay theo chiều kim đồng hồ hoặc ngược chiều kim đồng hồ.",
    controls: "Gõ CLLWISE hoặc COTER-CW.",
    walkthrough: [
      "Theo dõi hướng quay bánh xe mà mũi tên hoạt hình chỉ ra.",
      "Theo dõi sự kết nối đến các bánh răng bên cạnh (các bánh răng cưa quay ngược hướng, các dây an toàn mở giữ hướng đi, qua thắt lưng theo hướng ngược lại).",
      "theo chuỗi chuyển tiếp đến thiết bị cuối cùng và đưa ra câu trả lời.",
    ],
    strategies: [
      "Thay đổi hướng đi cho mọi điểm liên lạc bị chặn.",
      "Các vành đai bảo tồn hướng quay trừ khi chúng đi qua trong một chiếc X.",
    ],
  ),
  "continuous_paired_associate": (
    objective: "Học hai biểu tượng trừu tượng và chọn đối tác phù hợp khi có dấu chấm phẩy.",
    controls: "Ấn nút biểu tượng khớp với biểu tượng nhanh.",
    walkthrough: [
      "Hãy nghiên cứu các liên kết biểu tượng trong giai đoạn học đếm ngược.",
      "Tạo ra một ký hiệu tâm thần kết nối mỗi biểu tượng dấu hiệu với bạn tình của nó.",
      "Khi được thăm dò với một dấu hiệu, hãy gõ vào mục tiêu khớp từ khay.",
    ],
    strategies: [
      "Phát minh ra những câu chuyện hình ảnh liên kết hai ký hiệu (ví dụ, ' sao nạp nhiên liệu cho tên lửa'.",
      "Hãy chú ý đến những điểm nổi bật màu sắc.",
    ],
  ),
  "kurodoko": (
    objective: "Đặt các tế bào đen trên lưới để mỗi ô màu trắng đánh số thấy số chính xác của bạch cầu hay othogonly.",
    controls: "Đập một buồng trống một lần để đánh dấu trắng, gõ hai lần để đánh dấu đen.",
    walkthrough: [
      "Kiểm tra manh mối đánh số; mỗi ô chỉ ra có thể thấy có bao nhiêu bạch cầu theo chiều ngang và dọc.",
      "bảo đảm không có hai tế bào đen nào chạm vào hoặc không chạm vào.",
      "Giữ cho tất cả bạch cầu kết nối với một nhóm riêng lẻ.",
    ],
    strategies: [
      "Các tế bào với các đầu mối lớn phải có hành lang trắng không thể phá vỡ lâu dài.",
      "Không thể che mờ manh mối.",
      "Nếu một tế bào là màu đen, tất cả bốn nhà hàng xóm phải màu trắng.",
    ],
  ),
  "subitizing_rush": (
    objective: "Ngay lập tức nhận ra số lượng các chấm nhấp nháy mà không cần đếm số lẻ.",
    controls: "Ấn nút số khớp.",
    walkthrough: [
      "Tập trung nhìn vào trung tâm của bức tranh.",
      "Khi các dấu chấm nhấp nháy, hãy nắm bắt các mô hình như một nhóm thị giác toàn diện.",
      "Chọn chính xác số điểm bạn quan sát.",
    ],
    strategies: [
      "Một nhóm chấm tâm trí thành những cụm nhỏ gồm 2, 3, hay 4.",
      "Đừng đếm từng người một; hãy dựa vào nhận thức thị giác nhanh.",
    ],
  ),
  "action_sequence_recall": (
    objective: "Hãy quan sát một chuỗi cử chỉ ký tự và lặp lại theo thứ tự chính xác mà chúng được hiển thị.",
    controls: "Đạp các nút hành động tương ứng để tua lại chuỗi.",
    walkthrough: [
      "Quan sát: Xem ký tự thực hiện một chuỗi các điệu bộ hoạt hình (ví dụ vẫy tay, nhảy, cúi chào).",
      "Ghi nhớ: ghi nhớ mỗi cử chỉ khi nó xảy ra, tạo ra tên viết tắt cho mỗi (ví dụ 'W-J-B').",
      "Khi chuỗi kết thúc và đầu vào được mở khóa, hãy nhấn nút hành động theo cùng thứ tự.",
    ],
    strategies: [
      "Nói lớn tiếng hành động hoặc lặp đi lặp lại theo nhịp trong đầu.",
      "Gán thẻ ngắn hình ảnh đơn giản cho mỗi chuyển động.",
      "Đừng click vội; đợi cho trình tự đầy đủ hoàn thành trước khi bắt đầu nhập.",
    ],
  ),
  "affix_factory": (
    objective: "Hãy chọn chuỗi chính xác gắn vào một từ cơ sở đã cho để tạo một từ hợp lệ mới.",
    controls: "Gõ đúng nút Affix từ nhiều tùy chọn được cung cấp.",
    walkthrough: [
      "Đọc từ cơ bản được hiển thị ở giữa màn hình.",
      "Hãy nhìn vào các tùy chọn đa kênh (ví dụ, 'un-, '-ly','re-).",
      "Quyết định xem bản cam kết nào có thể hợp pháp gắn liền với chữ cơ bản.",
      "Hãy gõ đúng từ ngữ để xây dựng từ mới và tiến tới câu đố tiếp theo.",
    ],
    strategies: [
      "Cố gắng nói lớn tiếng từ trong đầu bạn để xem nó có giống như một từ thật không.",
      "Hãy chú ý đến vị trí dấu gạch nối để biết bạn đang chọn tiền tố (trước) hay hậu tố (sau đó).",
      "Loại bỏ rõ ràng các bản cam kết sai mà vi phạm các quy tắc chính tả chuẩn tiếng Anh.",
    ],
  ),
  "akari": (
    objective: "Đặt bóng đèn để chiếu sáng mỗi ô trống trong lưới mà không có hai bóng đèn chiếu vào nhau.",
    controls: "Mở một buồng giam trống để đặt một bóng đèn, gõ vào một bóng đèn đặt sẵn để gỡ bỏ nó.",
    walkthrough: [
      "Tìm các ô màu đen có số. Số này cho biết chính xác phải đặt bao nhiêu bóng đèn kề bên (trên, dưới, trái, phải) vào ô đó.",
      "Đặt bóng đèn xung quanh các tế bào đánh số nơi vị trí bị ép (ví dụ, a '4' cần một bóng đèn ở bốn mặt).",
      "Ánh sáng chiếu sáng toàn bộ hàng và cột vào cạnh lưới hoặc khối tế bào đen.",
      "Chắc chắn không có hai bóng đèn chiếu sáng lẫn nhau.",
      "Tiếp tục đặt bóng đèn cho đến khi mọi ô trắng trống được chiếu sáng.",
    ],
    strategies: [
      "Bắt đầu với số cao nhất ('4' hoặc '3) vì chúng thường có các tùy chọn định giới hạn hoặc ép buộc.",
      "Nếu một khối 0 có trên mạng lưới, bạn biết không có bóng đèn nào được đặt cạnh nó.",
      "Tìm những tế bào lẻ loi chỉ có thể được chiếu sáng bởi một bóng đèn đặt ở chính vị trí đó hoặc hàng/column.",
    ],
  ),
  "algebraic_balance": (
    objective: "Vẽ giá trị số của một hình mục tiêu cụ thể bằng cách phân tích các phương trình cân bằng thị giác.",
    controls: "Dùng bộ lọc số ảo để nhập vào giá trị đã tính, rồi bấm cái nút Gửi.",
    walkthrough: [
      "Kiểm tra cán cân thăng bằng cho thấy các hình dạng khác nhau cân bằng trọng lượng mục tiêu hoặc mỗi cái khác.",
      "Xem các vảy như phương trình đại số (v. g., 2 tam giác + 1 Circle = 15).",
      "Giải quyết các giá trị riêng của các hình dạng bằng cách thay thế hoặc loại bỏ.",
      "Xác định giá trị của hình mục tiêu được đánh dấu bằng dấu câu hỏi.",
      "Hãy nhập vào giá trị chính xác của con số bằng cách dùng bảng số.",
    ],
    strategies: [
      "Hãy tìm một quy mô đơn giản nhất trước tiên, đặc biệt là một hình đơn lẻ (ví dụ, 3 hình vuông = 12 có nghĩa là hình vuông = 4).",
      "Thay thế các giá trị được biết thành các cấp cân phức tạp hơn để tìm những giá trị còn lại chưa rõ.",
      "Kiểm tra lại hai lần tính toán bằng cách cắm những câu trả lời cuối cùng vào cái cân để xem chúng có cân bằng không.",
    ],
  ),
  "alphabet_sudoku": (
    objective: "Điền một lưới 4x4 với bốn chữ cái riêng biệt để không có chữ cái lặp lại trong bất kỳ hàng, cột, hoặc 2x2 phụ thuộc.",
    controls: "Gõ vào một ô lưới trống, rồi gõ một lá thư từ thanh chọn bên dưới để lấp đầy xà lim.",
    walkthrough: [
      "Phân tích lưới 4x4 một phần và tập hợp bốn chữ cái đích.",
      "Tìm một hàng, cột, hoặc 2x2 khối mà chỉ thiếu một chữ cái và điền vào.",
      "Dùng quá trình loại bỏ để tìm các tế bào mà chỉ có thể đặt một chữ cái đặc trưng mà không vi phạm các quy tắc của đảo Sudoku.",
      "Tiếp tục làm đầy các tế bào cho đến khi toàn bộ lưới được hoàn tất và hợp lệ.",
    ],
    strategies: [
      "Tập trung vào phụ đề 2x2, vì chúng thường là nơi dễ nhất để phát hiện những lá thư bị mất.",
      "Tham chiếu chéo các ô rỗng bằng cách kiểm tra cả các hạn chế hàng ngang và cột dọc.",
      "Nếu bạn bị mắc kẹt, hãy tìm một chữ cái cụ thể và xem những tế bào nào trong lưới mà nó bị chặn không cho vào.",
    ],
  ),
  "anagram_definition": (
    objective: "Bỏ đi một tập hợp các chữ cái cho phép tạo thành một từ khớp với định nghĩa từ điển đã đưa ra.",
    controls: "Gõ các chữ cái trộn vào đúng theo thứ tự để đánh vần chữ. Gõ vào các chữ để gỡ bỏ chúng, hoặc dùng cái nút rõ ràng.",
    walkthrough: [
      "Đọc định nghĩa được cung cấp cẩn thận để hiểu ý nghĩa của từ mục tiêu.",
      "Hãy nhìn vào các miếng chữ cái trộn dưới định nghĩa.",
      "Tâm trí sắp xếp các chữ cái để tìm một từ phù hợp với định nghĩa.",
      "Gõ các chữ cái để đánh vần câu trả lời.",
      "Nếu không đúng, hãy dọn sạch đầu vào và thử một sự sắp đặt khác.",
    ],
    strategies: [
      "Tìm kiếm các tiền tố chung (như 'un-', 're-') hoặc hậu tố (như '-ing', '-d', '-tion') giữa các chữ cái trộn.",
      "Nếu bạn đang bị mắc kẹt vào các chữ cái, tập trung hoàn toàn vào định nghĩa và suy nghĩ của đồng nghĩa.",
      "Nhận diện các nguyên âm trước và thử đặt chúng theo mẫu điển hình.",
    ],
  ),
  "angle_finder": (
    objective: "Ước tính và tái tạo góc mục tiêu bằng cách điều chỉnh cánh tay giả.",
    controls: "Kéo con trượt ở dưới màn hình để điều chỉnh góc của cánh tay dao động.",
    walkthrough: [
      "Nhìn vào giá trị góc đích (ví dụ, 45 °, 120 °) được hiển thị trên màn hình.",
      "Hãy hình dung góc đó giống góc nào so với góc vuông 90 ° hoặc 180 °.",
      "Kéo con trượt để xoay cánh tay động cho đến khi góc nhìn khớp với ước tính của bạn.",
      "Nhấn nút 'Lấp' để khóa trong đoán.",
      "Nhắm đến độ chính xác cao để tối đa hóa điểm số của bạn trên nhiều viên đạn.",
    ],
    strategies: [
      "Sử dụng góc chuẩn: 90 ° là một L-shape hoàn hảo, 180 ° bằng phẳng, 45 ° chính xác là giữa 0 và 90.",
      "Nếu mục tiêu là 135 °, hãy nghĩ nó là 90 ° và thêm 45 ° nữa.",
      "Hãy điều chỉnh nhỏ, khéo léo bằng cách dùng con trượt trước khi đưa ra câu trả lời cuối cùng.",
    ],
  ),
  "area_perimeter_match": (
    objective: "Điều chỉnh kích thước của hình chữ nhật cho đến khi khu vực của nó và vành đai phù hợp với các giá trị mục tiêu cho trước.",
    controls: "Nhấn nút '+' và '-' ở bên hình chữ nhật để tăng hay giảm chiều rộng và chiều cao của nó.",
    walkthrough: [
      "Lưu ý vùng mục tiêu (Width × cao) và vùng phụ cận (× (Width + high).",
      "Quan sát kích thước hiện tại của hình chữ nhật trên màn hình.",
      "Dùng điều khiển « + » và «- » để thay đổi chiều rộng và chiều cao.",
      "Tìm hai yếu tố cụ thể mà nhân với khu vực mục tiêu và thêm lên đến một nửa chu vi mục tiêu.",
      "Trò chơi tự động hoàn tất vòng khi các chiều không gian chính xác đã đạt đến.",
    ],
    strategies: [
      "Tập trung vào khu vực đầu tiên bằng cách tìm các cặp số (ví dụ, nếu diện tích là 24, cặp là 1x24, 2x12, 3x8, 4x 6).",
      "Một khi bạn có một cặp yếu tố, kiểm tra xem vành đai của nó có phù hợp với mục tiêu không.",
      "Một hình vuông (hoặc gần vuông) giảm thiểu chu vi cho một khu vực nhất định, trong khi một hình chữ nhật dài, mỏng tối đa hóa nó.",
    ],
  ),
  "arithmetic_chain": (
    objective: "Hãy giữ tổng số chạy trong đầu bạn như một chuỗi các hoạt động số học được hiển thị, và tính toán kết quả cuối cùng.",
    controls: "Dùng bảng số ảo để nhập vào câu trả lời được tính toán cuối cùng, rồi tap submit.",
    walkthrough: [
      "Hãy nhớ số bắt đầu hiện trên màn hình.",
      "Xem như một chuỗi các thao tác toán học (ví dụ, '+3','× 2', '-4) xuất hiện.",
      "Thực hiện mỗi tính toán trên tổng chạy của bạn khi nó xuất hiện.",
      "Một khi chuỗi kết thúc, hãy nhập giá trị tính toán cuối cùng bằng cách sử dụng miếng số.",
    ],
    strategies: [
      "Đừng lo lắng về việc ghi nhớ từng bước một, chỉ tập trung hoàn toàn vào việc cập nhật toàn bộ hiện tại của bạn.",
      "Hãy bình tĩnh trong quá trình nhân hay chia, vì chúng thường tạo ra các số nguyên sạch.",
      "Hãy kiểm tra hai lần tính toán trí tuệ cuối cùng trước khi đăng ký.",
    ],
  ),
  "associative_pairs": (
    objective: "Hãy nhớ lại sự kết hợp giữa các màu sắc và hình dạng cụ thể, và nhớ lại chính xác khi bị thử thách.",
    controls: "Gõ chính xác câu trả lời từ các lựa chọn đa chọn được cung cấp trong giai đoạn thu hồi.",
    walkthrough: [
      "Xem màn hình như những cặp màu và hình dạng được trình bày bởi một người trong giai đoạn ghi nhớ.",
      "Tạo một liên kết tinh thần giữa các hình và màu (ví dụ, 'Teal Square').",
      "Sau khi bài thuyết trình kết thúc, một câu hỏi gợi nhớ sẽ xuất hiện khi hỏi xem màu nào liên quan đến một hình dạng cụ thể.",
      "Chọn màu đúng từ các tùy chọn sẵn sàng để ghi điểm.",
    ],
    strategies: [
      "Hãy tạo ra một câu chuyện nhanh chóng hoặc hình ảnh minh họa cho mỗi cặp (ví dụ, hình dung một vòng tròn sáng như mặt trời).",
      "Lặp lại những cặp đôi lớn hoặc trong đầu của bạn khi chúng xuất hiện trên màn hình.",
      "Đừng để những màu tương tự (như Teal và Blue) làm bạn bối rối; tập trung vào những thẻ trí tuệ khác nhau.",
    ],
  ),
  "attentional_blink": (
    objective: "Xác định hai con số chỉ xuất hiện trong một chuỗi chữ cái liên tục và nhanh chóng.",
    controls: "Dùng bàn phím để gõ số mục tiêu thứ nhất và thứ hai bạn thấy, rồi nộp.",
    walkthrough: [
      "Nhắm mắt vào trung tâm màn hình như một dòng chữ nhanh chóng nhấp nháy.",
      "Hãy cảnh giác và tìm con số đầu tiên (Target 1) ẩn trong số các chữ cái.",
      "Lập tức chuẩn bị nhận ra con số thứ hai (Target 2) sẽ xuất hiện ít lâu sau đó.",
      "Một khi chuỗi kết thúc, hãy gõ cả hai số theo thứ tự bạn thấy chúng.",
    ],
    strategies: [
      "Đừng di chuyển mắt, hãy tập trung vào đúng vị trí của các ký tự.",
      "Hãy cẩn thận với \"cái chớp mắt\" một chút sau khi phát hiện ra con số đầu tiên, bộ não của bạn sẽ bỏ lỡ cái thứ hai nếu nó xuất hiện quá nhanh.",
      "Hãy nói số đầu tiên lớn lên ngay khi bạn thấy nó để giải phóng sự chú ý thị giác của bạn cho số thứ hai.",
    ],
  ),
  "balance_scale": (
    objective: "Vẽ khối lượng của mục tiêu dựa trên phương trình cân bằng thị giác.",
    controls: "Dùng bảng số ảo để gõ câu trả lời đã tính, rồi bấm cái nút Đăng ký checkmark.",
    walkthrough: [
      "Xem lại các cán cân cân cân được hiển thị trên màn hình. Mỗi thang đại diện cho một phương trình toán học.",
      "Xác định giá trị khối lượng đã biết (thường được tượng trưng bởi số lượng hay hình dạng chuẩn)",
      "Dùng khả năng thay thế để tìm trọng lượng của các mục chưa biết trên cân.",
      "Xác định trọng lượng của mục tiêu được đánh dấu bằng dấu câu hỏi.",
      "Hãy nhập vào câu trả lời đã suy luận của bạn bằng cách dùng bảng số.",
    ],
    strategies: [
      "Tìm tỷ lệ giữa các mục giống hệt nhau cân bằng một số đã biết để nhanh chóng thiết lập một giá trị cơ bản.",
      "Xử lý tỷ lệ chính xác như phương trình đại số. Nếu 2 mục cân bằng 10, thì 1 là 5.",
      "Làm việc một cách có phương pháp từ quy mô đơn giản nhất đến cái phức tạp nhất.",
    ],
  ),
  "base_conversion_run": (
    objective: "Chuyển đổi một số từ lúc khởi động cơ sở vô tính (ví dụ, Biary, Hex) thành một cơ sở mục tiêu.",
    controls: "Gõ chính xác số chuyển đổi từ 4 lựa chọn đa chọn.",
    walkthrough: [
      "Hãy nhìn vào lá bài đầu tiên để xem con số bắt đầu và cơ sở (e.g., Binary, Octal, Decimal, Henum).",
      "Hãy lưu ý đến cơ sở của mục tiêu mà bạn cần chuyển số thành số.",
      "Thực hiện chuyển đổi tâm trí cơ bản hoặc dùng giấy cào.",
      "Gõ giá trị chuyển đổi chính xác từ các tùy chọn ở dưới màn hình để ghi điểm.",
    ],
    strategies: [
      "Khi chuyển sang hai giai đoạn, hãy nhớ sức mạnh của 2 (1, 2, 4, 8, 16, 32).",
      "Với thập lục phân, hãy nhớ rằng chữ A-F tượng trưng cho giá trị 10-15.",
      "Nếu bạn bị mắc kẹt, hãy thử chuyển đổi con số bắt đầu thành chữ số thập phân (Base 10) trước, như một bước trung gian.",
    ],
  ),
  "base_shift": (
    objective: "Giải một biểu thức số học liên quan đến số trong các cơ số khác nhau và nhập kết quả thập phân chính xác.",
    controls: "Gõ vào ô văn bản để mở bàn phím, gõ câu trả lời số tính toán và nhấn nút Gửi.",
    walkthrough: [
      "Đọc cụm từ số học được cung cấp trên màn hình.",
      "Biểu thức sẽ bao gồm số trong các cơ số khác nhau (được in bởi các tiền tố như '0x' cho Hex hoặc '0b' cho nhị phân).",
      "Chuyển đổi các con số sang số thập phân chuẩn (cơ số 10).",
      "Thực hiện thao tác toán học đã yêu cầu.",
      "Nhập kết quả thập phân cuối cùng và phục tùng.",
    ],
    strategies: [
      "Ghi nhớ các giá trị cơ bản của thập lục phân (0xA = 10, 0xF = 15) để tăng tốc độ chuyển đổi.",
      "Đối với nhị phân, nhanh chóng thêm các bit hoạt động (e.g., 0b1011 = 8 + 0 + 2 + 1 = 11).",
      "Luôn chuyển thành thập phân trước khi thử phép cộng hay trừ.",
    ],
  ),
  "binary_code": (
    objective: "Dịch nhanh chóng các chuỗi nhị phân 4 bit vào các giá trị nguyên số thập phân chuẩn.",
    controls: "Gõ chính xác số thập phân từ lưới 2x2 tùy chọn đa chọn.",
    walkthrough: [
      "Xem chuỗi nhị phân 4- bit (ví dụ, '1011' được hiển thị ở giữa màn hình.",
      "Tính giá trị thập phân bằng cách xác định các mũ 2 (8, 4, 2, 1) có mặt ở đây.",
      "Tìm giá trị thập phân tương ứng trong lưới tùy chọn bên dưới.",
      "Nhấn đúng lựa chọn càng nhanh càng tốt trước khi hết giờ.",
    ],
    strategies: [
      "Ghi nhớ các giá trị tiêu chuẩn 4 bit: con số đầu tiên là 8, con số thứ hai là 4, thứ ba là 2, thứ tư là 1.",
      "Đối với '11', biết ngay lập tức rằng nó bằng 15. Đối với '2000', biết nó bằng 8.",
      "Tốc độ là chìa khóa trong trò chơi chạy nước rút này; hãy tin tưởng toán học nhanh trí tuệ của bạn và gõ ngay lập tức.",
    ],
  ),
  "binary_puzzle": (
    objective: "Điền lưới bằng 0 và 1s để không có ba số giống hệt nhau kề nhau, mỗi hàng và cột có một số bằng nhau của 0 và 1, và tất cả các hàng và cột là độc nhất.",
    controls: "Gõ một ô rỗng hoặc chỉnh sửa để chuyển đổi giá trị của nó giữa rỗng, 0 và 1.",
    walkthrough: [
      "Kiểm tra lưới tìm số bắt đầu cố định.",
      "Tìm hai cặp số giống hệt nhau (ví dụ, '1-1'). Các tế bào ở hai bên phải là số đối diện (v. g., '0-1--0').",
      "Tìm con số giống hệt nhau được chia bởi một ô rỗng (ví dụ, '1- 1- 1). Tế bào rỗng phải là số đối diện ('1-0-1').",
      "Kiểm tra từng hàng và cột chứa chính xác nửa số 0 và nửa số 1.",
      "Chắc chắn không có hai hàng nào giống hệt nhau và không có hai cột nào giống hệt nhau.",
      "Tiếp tục làm giảm giá trị của tế bào cho đến khi lưới được điền đúng.",
    ],
    strategies: [
      "Nếu một hàng hoặc cột đã đạt đến hạn ngạch tối đa 1, hãy điền vào các ô rỗng còn lại bằng 0s.",
      "So sánh những hàng hoặc cột gần hoàn tất với những hàng hoặc cột đã có để tránh tạo ra những hàng hoặc cột lặp lại.",
      "Luôn luôn áp dụng quy tắc 'không ba trong một hàng' đầu tiên, vì nó cung cấp các suy luận ngay lập tức.",
    ],
  ),
  "binary_scale_balance": (
    objective: "Chọn đúng sự kết hợp của khối nhị phân để khớp hoàn toàn trọng lượng đích trên tỷ lệ.",
    controls: "Gõ vào các khối nhị phân (32, 16, 8, 4, 2, 1) để bật hay tắt, rồi nhấn nút 'BALUD?' để đệ trình.",
    walkthrough: [
      "Kiểm tra trọng lượng của mục tiêu để cân bằng quy mô.",
      "Xem các khối lượng nhị phân có sẵn.",
      "Ngăn chặn để tăng giá trị của chúng vào trọng lượng hiện tại.",
      "Điều chỉnh sự lựa chọn của bạn cho đến khi trọng lượng hiện tại chính xác với trọng lượng của mục tiêu.",
      "Nhấn nút 'BALD' để xác minh câu trả lời và chuyển sang vòng tiếp theo.",
    ],
    strategies: [
      "Dùng phương pháp tham lam: Luôn chọn khối lớn nhất có thể nhỏ hơn hoặc bằng trọng lượng còn lại.",
      "Nếu trọng lượng đích là lẻ, bạn phải chọn khối '1'.",
      "Trò chơi này về cơ bản chuyển một số thập phân thành nhị phân; mỗi khối đại diện cho một bit \"1\".",
    ],
  ),
  "binomial_match": (
    objective: "Xác định dạng yếu tố chính xác của một biểu thức bậc hai.",
    controls: "Gõ vào cặp biomial chính xác từ danh sách đa loại.",
    walkthrough: [
      "Xem biểu thức bậc hai mở rộng (v. g., x2 + 5 x + 6) được hiển thị ở trung tâm.",
      "Xác định hai số nhân với nhau để tương đương với thuật ngữ hằng số (c) và thêm vào để bằng hệ số của thuật ngữ giữa (b).",
      "Xem lại các lựa chọn đa lựa chọn nhị phân.",
      "Gõ tùy chọn chứa hai số chính xác (e.g., (x + 2) (x + 3).",
    ],
    strategies: [
      "Hãy chú ý đến các dấu hiệu. nếu thuật ngữ hằng số là tích cực, cả hai số có cùng dấu hiệu.",
      "Nếu thuật ngữ giữa là tiêu cực nhưng hằng số là tích cực, cả hai yếu tố số phải là tiêu cực.",
      "Loại bỏ các tùy chọn một cách nhanh chóng bằng cách chỉ kiểm tra phép nhân của hai hằng số trong nhị thức.",
    ],
  ),
  "blink_detector": (
    objective: "Xác định khuôn mặt mục tiêu trong một mạng lưới nháy mắt hai lần, trong khi lờ đi khuôn mặt của người đánh lạc hướng chỉ nháy mắt một lần.",
    controls: "Quan sát mạng lưới, sau đó gõ vào mặt mà thể hiện hành vi 2 lần liên kết.",
    walkthrough: [
      "Cẩn thận với những gương mặt.",
      "Những gương mặt khác nhau sẽ ngẫu nhiên chớp mắt một lần để đánh lạc hướng bạn.",
      "Hãy luôn để mắt xem xét một khuôn mặt cụ thể mà chớp mắt hai lần liên tiếp.",
      "Một khi bạn nhận ra khuôn mặt hai mắt, hãy gõ nó để ghi điểm.",
      "Lặp lại quá trình này cho đến khi bạn đạt điểm mục tiêu.",
    ],
    strategies: [
      "Giữ cái nhìn thoải mái và tập trung vào lưới thay vì nhìn chằm chằm vào một khuôn mặt cụ thể.",
      "Sử dụng thị lực ngoại biên của bạn để phát hiện chuyển động, sau đó tập trung vào để xác minh nó là một chớp mắt đơn hoặc hai lần.",
      "Đừng vội vỗ, chờ đợi để chắc chắn bạn nhìn thấy hai hình nháy mắt.",
    ],
  ),
  "block_count_3d": (
    objective: "Xác định tổng số khối lập phương riêng biệt tạo thành một cấu trúc khối ba chiều phức tạp.",
    controls: "Kéo ngón tay qua ô xem 3D để xoay cấu trúc. Hãy dùng phần mềm ảo để nhập và nạp lại.",
    walkthrough: [
      "Kiểm tra cấu trúc khối ba chiều hiển thị trên màn hình.",
      "Kéo để xoay mô hình và xem nó từ các góc khác nhau để đảm bảo bạn không bỏ lỡ các khối ẩn.",
      "Đếm các khối, nhớ rằng bất cứ khối nào trên cột cao hơn phải được hỗ trợ bởi những khối bên dưới.",
      "Gõ tổng số khối bằng numpad ảo.",
      "Nhấn nút đệ trình để kiểm tra câu trả lời.",
    ],
    strategies: [
      "Một cột cao 3 khối góp phần vào tổng cộng.",
      "Xoay khung cảnh để nhìn thẳng xuống từ trên cao để dễ dàng đếm dấu chân cơ bản.",
      "Hãy đảm bảo rằng bạn có thể tìm ra những khối hoàn toàn được giấu ở trung tâm của một cấu trúc lớn hơn.",
    ],
  ),
  "block_escape": (
    objective: "Dọn đường để trượt khối mục tiêu ra khỏi lối ra bên phải bảng.",
    controls: "Kéo các khối dọc theo trục ngang hoặc dọc để chuyển chúng vào những khoảng trống.",
    walkthrough: [
      "Xác định khối mục tiêu riêng (thường có màu khác nhau) cần phải đến lối ra bên phải.",
      "Xác định các khối cản đường mục tiêu ra lối ra.",
      "Kéo các khối dọc và ngang ra khỏi đường để tạo ra một làn đường rõ ràng.",
      "Trượt khối mục tiêu qua lối ra để giải câu đố.",
    ],
    strategies: [
      "Làm ngược lại: nhìn vào lối ra và xác định khối nào chặn trực tiếp nó lại, sau đó tìm ra cách để di chuyển khối cụ thể đó.",
      "Các khối nằm ngang chỉ có thể di chuyển trái/phải, và các khối dọc chỉ có thể di chuyển lên/ xuống.",
      "Đôi khi bạn phải di chuyển một khối vào con đường của mục tiêu để tạm thời xáo trộn các khối khác xung quanh.",
    ],
  ),
  "block_stacking_physics": (
    objective: "Xếp các khối di chuyển trên nhau càng cao càng tốt bằng cách canh thời gian cho giọt nước của bạn rơi hoàn hảo.",
    controls: "Gõ bất cứ nơi nào trên màn hình để thả khối đang di chuyển.",
    walkthrough: [
      "Xem các khối hoạt động trượt qua lại trên cùng của chồng.",
      "Thời gian gõ để khối hoạt động thẳng đứng hoàn hảo với khối bên dưới.",
      "Khi bạn vỗ, khối sẽ rơi.",
      "Tiếp tục xếp chồng cho đến khi đạt đến độ cao mục tiêu để chiến thắng.",
      "Nếu bạn hoàn toàn trật mục tiêu, cái tháp sẽ sập và trò chơi kết thúc.",
    ],
    strategies: [
      "Tập trung mắt bạn vào các cạnh của khối văn phòng phía dưới, và gõ chính xác khi cạnh của khối di chuyển liên tục với nó.",
      "Khi các khối trở nên nhỏ hơn, trò chơi trở nên khó khăn hơn; ưu tiên sự thẳng hàng hoàn hảo ngay từ đầu.",
      "Đi vào nhịp điệu, khi tốc độ khối tăng lên một chút với mỗi giọt thành công.",
    ],
  ),
  "box_completion": (
    objective: "Quyết định khối 3D nào được hình thành bằng cách gấp một lưới 2 chiều với số trên nó.",
    controls: "Gõ chính xác khối lập phương 3D từ các lựa chọn đa chọn được cung cấp.",
    walkthrough: [
      "Phân tích lưới 2D có hình chữ số trên mặt.",
      "Trong tâm trí bạn hãy gấp lưới thành một khối lập phương 3 chiều.",
      "Chú ý đến định hướng tương đối của các con số khi gấp lại.",
      "Nhìn vào các tùy chọn khối ba chiều đa kênh.",
      "Chọn khối khớp với mẫu tinh thần của lưới gấp.",
    ],
    strategies: [
      "Tìm những gương mặt đối lập trên lưới (mặt bị phân cách bởi một hình vuông). Chúng không bao giờ có thể ở cạnh khối cuối cùng.",
      "Chọn một mặt trước trên lưới và hình dung những gì con số gấp lại thành đầu, dưới, trái và phải vị trí.",
      "Sử dụng tiến trình loại bỏ để loại bỏ khối lập phương hiển thị những khuôn mặt không thể bên cạnh.",
    ],
  ),
  "bridges": (
    objective: "Kết nối tất cả các đảo thành một mạng liên tục với những cây cầu, bảo đảm cho mỗi hòn đảo có chính xác số cây cầu được chỉ ra bởi con số của nó.",
    controls: "Gõ một hòn đảo để chọn nó, rồi gõ một hòn đảo kế bên để vẽ một cây cầu.",
    walkthrough: [
      "Hãy xem lại những hòn đảo được đánh số trên mạng lưới.",
      "Gõ một hòn đảo để chọn nó, rồi gõ một orthogonal (lên, xuống, trái, phải) để kết nối chúng với một cây cầu.",
      "Cầu không thể băng qua cầu hay hải đảo khác.",
      "Mỗi đảo phải có tổng số cầu nối bằng con số của nó.",
      "Tất cả các đảo phải được kết nối với nhau trong một nhóm riêng lẻ để giải câu đố.",
    ],
    strategies: [
      "Hãy tìm những góc với '4', cạnh với '6', hay đảo giữa với '8'. Những thứ này cần thiết hai cầu trong tất cả các hướng sẵn sàng.",
      "Nếu một hòn đảo '1' được kết nối, không một cây cầu nào khác có thể gắn vào nó.",
      "Bảo đảm rằng bạn không tạo ra một vòng lặp khép kín của đảo; mạng lưới phải được kết nối hoàn toàn.",
    ],
  ),
  "calculation_sprint": (
    objective: "Giải quyết càng nhiều phương trình toán học càng tốt trước khi thời gian hết.",
    controls: "Hãy gõ chính xác câu trả lời từ hệ thống 2x2 của các lựa chọn đa chọn.",
    walkthrough: [
      "Bắt đầu đếm ngược.",
      "Đọc phương trình toán học được trình bày ở giữa màn hình.",
      "Tính toán nhanh câu trả lời.",
      "Gõ tùy chọn tương ứng từ các lựa chọn dưới đây.",
      "Đáp ứng đúng cách để tăng điểm và đạt được mục tiêu trước khi thời gian chấm dứt.",
    ],
    strategies: [
      "Đừng suy nghĩ quá nhiều, hãy dựa vào những phản ứng toán học nhanh chóng của bạn.",
      "Sử dụng ước tính hoặc nhìn vào số cuối cùng của các con số để nhanh chóng loại bỏ các tùy chọn đa lựa chọn sai.",
      "Giữ nhịp độ ổn định và đừng hoảng sợ nếu bạn phạm sai lầm.",
    ],
  ),
  "card_counting_memory": (
    objective: "Ghi nhớ một chuỗi các bài đã được chia và nhớ chính xác có bao nhiêu quân bài xuất hiện.",
    controls: "Đánh số chính xác từ các lựa chọn đa chọn trong giai đoạn thu hồi.",
    walkthrough: [
      "Bắt đầu giao dịch.",
      "Xem kỹ 5 lá bài được đưa lên màn hình.",
      "Theo dõi các bộ đồ (tiếng nghe, kim cương, câu lạc bộ, bích) của các quân bài.",
      "Sau khi giải quyết xong, một câu hỏi sẽ hỏi xem có bao nhiêu quân bài được bày ra.",
      "Hãy gõ đúng số để trả lời câu hỏi và ghi điểm.",
    ],
    strategies: [
      "Thay vì học thuộc lòng toàn bộ thẻ, hãy kiểm tra tâm trí (e.g., '2 Trái tim, 1 Spade, 2 câu lạc bộ') khi họ được đối xử.",
      "Đưa ngón tay lên bàn tay của bạn cho các bộ quần áo khác nhau và gõ chúng để giữ đếm.",
      "Hoàn toàn bỏ qua các hàng quân bài (số/ ký tự); chỉ tập trung vào các hình và màu sắc của bộ điều khiển.",
    ],
  ),
  "category_fluency": (
    objective: "Hãy gõ càng nhiều từ càng tốt phù hợp với loại đã chọn trước khi thời gian hết.",
    controls: "Dùng bàn phím để gõ chữ vào trường văn bản, rồi gõ vào biểu tượng gửi hoặc bấm nhấn vào bàn phím.",
    walkthrough: [
      "đọc dấu nhắc phân loại (ví dụ, dấu 'Animal','Frut''') ở đầu màn hình.",
      "Gõ vào ô nhập văn bản để mở bàn phím.",
      "Hãy nghĩ đến một từ thích hợp với loại chữ này, gõ và gởi đi.",
      "Từ ngữ hợp lệ sẽ được chấp nhận và thêm vào danh sách của bạn như thẻ.",
      "Hãy đếm từ đếm ngược trước khi đồng hồ đếm ngược đếm ngược đến 0 để thắng.",
    ],
    strategies: [
      "Hãy suy nghĩ trong tiểu phân (ví dụ, cho 'Animal', nghĩ về thú nuôi, sau đó trang trại, sau đó động vật sở thú) để chạy bộ bộ bộ nhớ của bạn.",
      "Gõ một cách nhanh chóng và không lo lắng về việc nhập các từ phức tạp, đơn giản, từ phổ biến chỉ có điểm như nhau.",
      "Nếu bạn bị mắc kẹt, hãy nhìn xung quanh môi trường ngay lập tức của bạn hoặc suy nghĩ thông qua bảng chữ cái để cảm hứng.",
    ],
  ),
  "chain_reaction": (
    objective: "Xây dựng chuỗi dài nhất có thể được bằng cách nhập những từ bắt đầu với hai chữ cuối cùng của từ trước.",
    controls: "Dùng bàn phím để gõ một từ vào trường văn bản, rồi gõ vào biểu tượng bổ sung hoặc nhấn vào bàn phím.",
    walkthrough: [
      "Hãy nhìn từ cuối cùng hiện đang ở dưới cùng của chuỗi.",
      "Hãy xác định hai chữ cái cuối cùng của từ này, được nhấn mạnh.",
      "Hãy nghĩ đến một từ tiếng Anh hợp lệ mới bắt đầu với hai chữ cái chính xác.",
      "Gõ chữ vào trường nhập và gửi nó để phát triển chuỗi.",
      "Giữ dây xích càng lâu càng tốt trước khi thời gian chấm dứt.",
    ],
    strategies: [
      "Giữ các từ tương đối ngắn để tiết kiệm thời gian gõ, vì điểm này dựa trên độ dài chuỗi chứ không phải độ phức tạp từ.",
      "Tránh sử dụng từ kết thúc bằng hai chữ cái hiếm (như 'x' hoặc 'uz') mà sẽ làm cho bước đi tiếp theo của bạn rất khó khăn.",
      "Nếu bạn bị mắc kẹt, hãy thử thêm các hậu tố chung như 'er','ed'd', hoặc 'ing' vào một từ cơ bản nếu nó giúp thiết lập một kết thúc dễ dàng hơn.",
    ],
  ),
  "chalk_and_talk": (
    objective: "Hãy lắng nghe và đánh đúng từ ngữ, lờ đi những từ gây phân tâm được viết trên bảng.",
    controls: "Gõ vào trường văn bản để mở bàn phím và gõ từ có thể nghe được. Gõ '- phục tùng' để xác nhận.",
    walkthrough: [
      "trò chơi đưa ra một từ \"nghe\" và một từ đánh lạc hướng hình ảnh trên bảng phấn.",
      "Bỏ qua từ hình ảnh.",
      "Gõ từ bạn nghe vào trường nhập.",
      "hoàn thành cho 5 vòng để kết thúc trận đấu.",
    ],
    strategies: [
      "Tập trung hoàn toàn vào tín hiệu âm thanh chứ không phải bảng.",
      "Hãy đọc kỹ văn bản của \"You HEAR\" nếu âm thanh bị tắt.",
      "Hãy gõ chính xác để tránh mất điểm trong việc phục tùng sai.",
    ],
  ),
  "change_blindness": (
    objective: "Xác định sự khác biệt giữa hai ảnh luân phiên trước khi thời gian hết.",
    controls: "Đánh dấu khu vực trên hình ảnh nơi bạn nhận thấy sự thay đổi.",
    walkthrough: [
      "màn hình nhấp nháy giữa hai ảnh giống hệt nhau.",
      "Cẩn thận quét các hình ảnh để nhận ra hoặc biến mất.",
      "Gõ vào vùng thay đổi.",
      "Tìm sự thay đổi qua nhiều vòng để chiến thắng.",
    ],
    strategies: [
      "Hãy tập trung vào từng phần của pho tượng mỗi lần.",
      "Tìm kiếm những vật đột nhiên xuất hiện hoặc biến mất.",
      "Đừng gõ ngẫu nhiên, vì các cú gõ sai có thể phạt bạn.",
    ],
  ),
  "chimp_test": (
    objective: "Ghi nhớ vị trí của con số và gõ chúng theo thứ tự liên tục sau khi chúng bị ẩn.",
    controls: "Hãy gõ các ô vuông ẩn theo thứ tự số chính xác.",
    walkthrough: [
      "Một lưới số được hiển thị ngắn trên màn hình.",
      "Hãy ghi nhớ vị trí của họ.",
      "Gõ '1' để bắt đầu; các số khác sẽ ẩn.",
      "Gõ vào những ô trống còn lại theo thứ tự liên tục.",
    ],
    strategies: [
      "Nhóm các con số thành mẫu hoặc hình dạng trong tâm trí bạn.",
      "Tập trung mạnh mẽ trong giai đoạn ghi nhớ ngắn ngủi.",
      "Hãy dành thời gian để nhớ lại, một sai lầm duy nhất sẽ kết thúc hiệp đấu.",
    ],
  ),
  "choice_reaction_time": (
    objective: "Phản ứng càng nhanh càng tốt đối với một kích thích thị giác bằng cách chọn một tùy chọn tương ứng đúng.",
    controls: "Ấn nút đúng (ví dụ, trái hay phải) khớp với kích thích được hiển thị.",
    walkthrough: [
      "Chờ hiệu ứng hình hoặc hướng xuất hiện trên màn hình.",
      "Nhận diện ngay bên hoặc nút nào tương ứng với.",
      "Nhấn nút đúng.",
      "Nhắc lại cho một số thử thách để có được một thời gian phản ứng trung bình.",
    ],
    strategies: [
      "Giữ ngón tay của bạn lơ lửng trên các nút.",
      "Tập trung vào trung tâm của màn hình để bạn có thể thấy sự kích thích ngay lập tức.",
      "Tính chính xác ưu tiên, vì chạm sai sẽ làm tổn thương điểm của bạn nhiều hơn là chậm lại một chút.",
    ],
  ),
  "classic_maze": (
    objective: "Di chuyển từ vị trí bắt đầu đến mục tiêu thông qua một mê cung phức tạp.",
    controls: "Đánh dấu theo hướng bạn muốn di chuyển ký tự, hoặc dùng các nút có hướng.",
    walkthrough: [
      "Xác định điểm bắt đầu và điểm kết thúc.",
      "Kéo lên, xuống, trái, hoặc phải để di chuyển.",
      "Tìm con đường mở mà không chạm vào ngõ cụt.",
      "đạt mục tiêu hoàn thành mê cung.",
    ],
    strategies: [
      "Tìm đường lùi từ mục tiêu bằng mắt trước khi di chuyển.",
      "Hãy nhìn trước những ngã tư để tránh những ngõ cụt dài.",
      "Di chuyển hiệu quả để hoàn thành mê cung trong ít nước đi hoặc ít thời gian hơn.",
    ],
  ),
  "cognate_catch": (
    objective: "Xác định những từ có ý thức (có nguồn gốc và ý nghĩa tương tự) trong nhiều ngôn ngữ khác nhau.",
    controls: "Đánh vào những từ có ý thức thực sự.",
    walkthrough: [
      "Một danh sách các cặp từ được trình bày.",
      "Quyết định cặp nào có cả gốc lẫn ý nghĩa.",
      "Chọn những nhận thức thực sự.",
      "Tránh những người bạn giả dối (những từ giống nhau nhưng có ý nghĩa khác).",
    ],
    strategies: [
      "Hãy tìm những tiền tố hoặc hậu tố chung.",
      "Hãy cẩn thận với những người bạn giả giữa các ngôn ngữ.",
      "Hãy phát âm những từ trong đầu bạn để tìm ra những điểm tương đồng về ngữ âm.",
    ],
  ),
  "collatz": (
    objective: "Hãy áp dụng các quy tắc phỏng đoán Collatz để đạt đến số 1 từ một số bắt đầu.",
    controls: "Gõ vào nút thao tác toán học tương ứng (ví dụ, 'n/2'\" hay '3n +').",
    walkthrough: [
      "bạn được cho một số nguyên bắt đầu.",
      "Nếu nó là chẵn, chia cho 2.",
      "nếu nó là lẻ, nhân 3 và thêm 1.",
      "Tiếp tục cho đến khi con số trở thành 1.",
    ],
    strategies: [
      "Hãy nhớ quy tắc: chẵn -> một nửa, lẻ -> 3n + 1.",
      "Tính toán cẩn thận để tránh những bước không cần thiết.",
      "Tìm sức mạnh của 2, khi chúng đi thẳng xuống còn 1.",
    ],
  ),
  "color_flood": (
    objective: "Làm ngập toàn bộ lưới bằng một màu duy nhất trong số lượng động tác được phép.",
    controls: "Gõ các nút màu ở phía dưới để thay đổi màu của cụm đang lớn của bạn.",
    walkthrough: [
      "Bắt đầu từ ô vuông góc trên bên trái.",
      "Chọn một màu khớp với các miếng kế bên để hấp thụ chúng.",
      "Tiếp tục thay đổi màu sắc để mở rộng diện tích.",
      "Điền toàn bộ bảng với một màu trước khi hết nước đi.",
    ],
    strategies: [
      "Luôn chọn màu hấp thụ tối đa các miếng mới.",
      "Hãy nhìn về phía trước để xem màu nào sẽ mở ra những phần lớn.",
      "Làm việc về phía rìa của bảng.",
    ],
  ),
  "color_match": (
    objective: "Xác định nếu nghĩa của từ khớp với màu mực thì nó được viết vào.",
    controls: "Gõ 'Có' nếu nó khớp, hoặc 'Không' nếu nó không khớp.",
    walkthrough: [
      "Một từ miêu tả màu xuất hiện trên màn hình.",
      "Xem màu thật của văn bản.",
      "Quyết định nếu từ ngữ trùng với màu.",
      "Trả lời nhanh chóng và chính xác trước nhiều thử thách.",
    ],
    strategies: [
      "Chủ yếu tập trung vào màu thị giác trước, sau đó đọc từ.",
      "Cố gắng ngắt kết nối bộ não đọc của bạn với quá trình xử lý thị giác.",
      "Đừng vội vã quá, như sai sót chi phí điểm.",
    ],
  ),
  "color_maze_nav": (
    objective: "Di chuyển mê cung bằng cách theo một trình tự cụ thể của các mảnh màu sắc.",
    controls: "Đánh dấu để chuyển ký tự của bạn vào ô vuông cạnh đó.",
    walkthrough: [
      "Theo dõi chuỗi màu cần thiết được hiển thị ở đầu trang.",
      "Di chuyển từ ô vuông đầu tiên sang ô vuông kế tiếp trong chuỗi.",
      "Tiếp tục lặp lại chuỗi khi bạn di chuyển.",
      "Đến lối ra mà không phá vỡ mô hình.",
    ],
    strategies: [
      "Luôn luôn kiểm tra hai lần màu tiếp theo cần thiết.",
      "Hãy lên kế hoạch trước vài bước để tránh những ngõ cụt.",
      "Nếu bạn bị mắc kẹt, hãy cẩn thận với bước đi của bạn.",
    ],
  ),
  "color_word_match_up": (
    objective: "Khớp màu mực của từ trên cùng với ý nghĩa của chữ dưới.",
    controls: "Gõ 'Match' hay 'Mis match' dựa trên điều kiện.",
    walkthrough: [
      "Hai từ được hiển thị trên màn hình.",
      "Xác định màu mực của từ trên cùng.",
      "Xác định ý nghĩa văn bản của từ dưới.",
      "Tap Match nếu chúng giống nhau, nếu không tap Mis match.",
    ],
    strategies: [
      "Phân biệt trong tâm trí hai nhiệm vụ: màu sắc cho đỉnh, đọc ở dưới.",
      "Bỏ qua đoạn trên cùng hoàn toàn.",
      "Hoàn toàn bỏ qua màu mực của từ dưới.",
    ],
  ),
  "common_denominator": (
    objective: "Tìm mẫu số chung thấp nhất (LCD) cho một tập phân số nhất định.",
    controls: "Gõ hay chọn đúng số rồi gởi.",
    walkthrough: [
      "Một tập hợp phân số được hiển thị.",
      "Xác định mẫu số của mọi phân số.",
      "Tính toán số phổ biến thấp nhất của những con số này.",
      "Hãy trả lời cho xong hiệp.",
    ],
    strategies: [
      "Kiểm tra xem mẫu số lớn nhất có phải là một số khác hay không.",
      "Sử dụng yếu tố chính cho số lớn hơn.",
      "Thực hành bảng nhân của bạn để tăng tốc độ tính toán.",
    ],
  ),
  "compass_maze": (
    objective: "Chuyển một lưới nơi bạn chỉ có thể di chuyển theo các hướng được chỉ ra bởi la bàn của ô vuông hiện thời.",
    controls: "Gõ một ô vuông kế bên theo hướng hợp lệ để di chuyển.",
    walkthrough: [
      "nhìn vào các mũi tên la bàn trên các ô vuông hiện tại.",
      "Chuyển sang ô vuông kế bên, thẳng hàng với một trong những mũi tên đó.",
      "Nhắc lại để tìm đường đến mục tiêu.",
      "Hãy đạt đến mục tiêu là chiến thắng.",
    ],
    strategies: [
      "Làm việc ngược từ mục tiêu để xem gạch nào chỉ tới nó.",
      "Tránh dùng mũi tên để tránh các đầu chết hoặc biên giới.",
      "Tìm những vòng thời gian và tránh bị mắc kẹt.",
    ],
  ),
  "complex_folding_nets": (
    objective: "Quyết định hình 3D nào có thể được hình thành bằng cách gấp lưới 2 chiều đã cung cấp.",
    controls: "Đánh đúng 3D tùy chọn.",
    walkthrough: [
      "Phân tích hình dạng 2 chiều đã mở (net).",
      "Tâm trí gấp mặt lại với nhau dọc theo cạnh.",
      "So sánh mô hình tinh thần của bạn với các hình ba chiều đa điểm.",
      "Chọn hình giống nhau.",
    ],
    strategies: [
      "Tập trung vào một khuôn mặt đặc biệt và theo dõi các cạnh của nó.",
      "Sử dụng quá trình loại bỏ cho những hình dạng rõ ràng là không thể.",
      "Hãy chú ý đến định hướng của các khuôn mặt.",
    ],
  ),
  "compound_connect": (
    objective: "Kết nối hai từ để tạo một từ hợp lệ.",
    controls: "Ghi lại từ danh sách đầu tiên, rồi nghe một từ từ danh sách thứ hai.",
    walkthrough: [
      "Hãy nhìn những mảnh vỡ được cung cấp.",
      "Xác định các cặp kết hợp để tạo ra một từ tổng hợp.",
      "Chọn nửa đầu, rồi nửa sau.",
      "Làm rõ mọi từ trong bảng.",
    ],
    strategies: [
      "Bắt đầu với những cặp rõ ràng nhất trước.",
      "Nếu một từ không phù hợp, hãy nghĩ về những ý nghĩa thay thế.",
      "Hãy đọc lớn tiếng những lời còn lại để xem chúng có hòa hợp với nhau không.",
    ],
  ),
  "conjunction_search": (
    objective: "Tìm mục đích cụ thể kết hợp hai tính năng riêng biệt giữa những người đánh lạc hướng.",
    controls: "Đánh trúng mục tiêu trên màn hình.",
    walkthrough: [
      "trò chơi cho bạn biết những gì cần tìm (ví dụ, 'Red Square').",
      "Quét lưới các bộ phân tâm (ví dụ, vòng tròn đỏ, ô vuông xanh dương).",
      "Xác định mục khớp cả hai tính năng.",
      "Bắt nó nhanh chóng để có được điểm.",
    ],
    strategies: [
      "Quét một cách có hệ thống (từ trái sang phải, từ trên xuống dưới).",
      "Tập trung vào việc tìm kiếm một tính năng trước, sau đó lọc theo thứ hai.",
      "Đừng để bị phân tâm bởi những thứ chỉ chia sẻ một tính năng.",
    ],
  ),
  "consonant_reconstruct": (
    objective: "Đoán xem từ ẩn chỉ dùng các phụ âm do nó cung cấp.",
    controls: "Gõ từ đầy đủ vào trường nhập.",
    walkthrough: [
      "Một từ được hiển thị thiếu nguyên âm.",
      "Dùng phụ âm còn lại làm manh mối.",
      "Điền các nguyên âm chính xác vào để tái tạo từ.",
      "Hãy trả lời.",
    ],
    strategies: [
      "Hãy tìm những tiền tố và hậu tố chung.",
      "Thử đưa các nguyên âm phổ biến như E hoặc A đầu tiên.",
      "Hãy nghĩ về các mô hình từ và cấu trúc âm thanh.",
    ],
  ),
  "context_clues": (
    objective: "Xác định ý nghĩa của một từ còn thiếu dựa trên ngữ cảnh chung quanh câu.",
    controls: "Hãy chọn từ tốt nhất từ các tùy chọn trắc nghiệm.",
    walkthrough: [
      "Đọc câu với khoảng trống.",
      "Phân tích ngữ cảnh và âm điệu của câu.",
      "Xem lại các lựa chọn.",
      "Nghe từ nào là tốt nhất để hoàn thành ý tưởng.",
    ],
    strategies: [
      "Tìm kiếm từ tín hiệu (như '' thế nào cũng được' hoặc '' 'bởi vì').",
      "Loại bỏ các lựa chọn sai ngữ pháp.",
      "Hãy đọc câu hoàn tất để xem câu này có hợp lý không.",
    ],
  ),
  "continuous_recognition": (
    objective: "Xác định nếu ảnh hiện có xuất hiện trước trong chuỗi này.",
    controls: "Gõ 'New' nếu đây là lần đầu tiên nhìn thấy nó, hoặc '' Old' nếu bạn đã từng thấy nó trước đây.",
    walkthrough: [
      "Hình ảnh sẽ xuất hiện trên màn hình từng cái một.",
      "Cho mỗi hình ảnh, quyết định xem nó là một món đồ mới hay một món đồ mới.",
      "Nhấn nút Mới hay cũ tương ứng.",
      "Tiếp tục theo dõi khi chuỗi ngày càng dài.",
    ],
    strategies: [
      "Hãy tập trung vào những chi tiết đặc biệt của mỗi hình ảnh để nhớ kỹ hơn.",
      "Tin tưởng vào phản ứng của bạn; suy nghĩ thái quá có thể dẫn đến những lỗi lầm.",
      "Hãy tập trung cao độ vào, vì một sai sót tạm thời có thể làm hỏng đường nét của bạn.",
    ],
  ),
  "corsi_blocks": (
    objective: "Ghi nhớ và sao chép một chuỗi các khối đã được khai thác theo thứ tự chính xác.",
    controls: "Mở các khối trong trình tự mà chúng phát sáng.",
    walkthrough: [
      "quan sát các khối này một cách cẩn thận khi chúng chiếu sáng từng khối một.",
      "Hãy nhớ quy luật và trật tự.",
      "Chờ chuỗi để kết thúc.",
      "Theo đúng thứ tự của các khối nhà.",
    ],
    strategies: [
      "Theo dõi mẫu có mắt hoặc ngón tay trong không khí.",
      "Kéo chuỗi thành các nhóm nhỏ hơn 3 hay 4 dãy nhà.",
      "Tập trung vào hình dạng hình học các hình thức chuỗi.",
    ],
  ),
  "countdown_math": (
    objective: "Sử dụng các con số cung cấp và các nhà toán học cơ bản để đạt được một số mục tiêu trước khi thời gian hết.",
    controls: "Những con số và nhà điều hành để xây dựng phương trình của bạn.",
    walkthrough: [
      "bạn được cung cấp một số mục tiêu và một tập hợp các số bắt đầu.",
      "Chọn một số, sau đó là một nhà điều hành, rồi một số khác.",
      "Kết quả trở thành một con số mới.",
      "Tiếp tục kết hợp cho đến khi đạt được mục tiêu chính xác.",
    ],
    strategies: [
      "Làm việc ngược từ số mục tiêu nếu có thể.",
      "Lưu những con số nhỏ vào lúc kết thúc.",
      "Đừng ngại làm sáng tỏ và bắt đầu lại nếu anh bị kẹt.",
    ],
  ),
  "crown": (
    objective: "Đặt vương miện trên mạng lưới để không chia đôi cùng một hàng, cột, hoặc khu vực màu sắc, và chúng không chạm chéo nhau.",
    controls: "Đập những ô rỗng vào vị trí hoặc gỡ bỏ vương miện, ấn dài để đánh dấu X.",
    walkthrough: [
      "Phân tích vùng màu trên mạng lưới.",
      "Đặt một cái vương miện ở mỗi vùng, hàng và cột.",
      "Mão triều thiên thậm chí không chạm chéo.",
      "Điền đầy những điểm cần thiết để giải câu đố.",
    ],
    strategies: [
      "Bắt đầu với những vùng nhỏ nơi mà các lựa chọn vị trí bị hạn chế.",
      "Dùng dấu X để gạch bỏ các tế bào không hợp lệ.",
      "Hãy nhớ rằng những góc cạnh nhau không hợp lệ.",
    ],
  ),
  "crypto_arithmetic": (
    objective: "Deduce mà số tương ứng với mỗi chữ cái để làm cho các phương trình toán học đúng.",
    controls: "Gõ một lá thư và dùng miếng số để gán cho nó một con số.",
    walkthrough: [
      "Xem phương trình dựa trên chữ cái (ví dụ, AB + A = BCC).",
      "Dùng logic để tìm ra những hạn chế về giá trị (ví dụ, C phải là 1).",
      "Gán số cho chữ cái.",
      "Giải câu đố để tính toán hợp lý.",
    ],
    strategies: [
      "Tìm người mang theo các hoạt động để tìm ra số 1 hoặc 0.",
      "Nhận diện những chữ cái bị hạn chế đầu tiên.",
      "Dùng phép thử và lỗi cho vài chữ số cuối cùng nếu cần.",
    ],
  ),
  "cryptogram": (
    objective: "Giải mã thông điệp đã được mã hóa bằng cách thay thế chữ cái.",
    controls: "Gõ một lá thư đã mã hóa và gán cho nó một lá thư thật từ bàn phím.",
    walkthrough: [
      "Phân tích đoạn mã và tần số chữ cái.",
      "Đoán xem những chữ thông thường như E, T hay A.",
      "điền vào những từ ngắn như 'THE' hoặc 'AND'.",
      "Hãy tiết lộ toàn bộ thông điệp bị giấu kín.",
    ],
    strategies: [
      "Hãy tìm những từ đơn viết thường là 'A' hoặc 'I'.",
      "Tìm những từ 2 chữ thông dụng (OF, TO, IN, IS).",
      "Kiểm tra xác suất kết thúc thông thường như 'S','t',' or 'll'.",
    ],
  ),
  "cube_net_fold": (
    objective: "Xác định cấu hình khối ba chiều nào khớp với lưới mở rộng hai chiều hiển thị.",
    controls: "Gõ vào tùy chọn khối lập phương 3D chính xác (A, B, hay C) ở dưới cùng màn hình, sau đó gõ SUBMIT CHOICE.",
    walkthrough: [
      "quan sát màu sắc trên màn hình 2 chiều.",
      "Hãy hình dung làm thế nào lưới được gấp lại thành một khối 3D.",
      "Kiểm tra ba chiều của các tùy chọn lập phương được cung cấp.",
      "Chọn khối đại diện cho độ xoay hợp lệ của lưới gấp và gửi sự lựa chọn của bạn.",
    ],
    strategies: [
      "Hãy nhìn những gương mặt đối diện trên lưới. Chúng sẽ có một hình vuông giữa chúng. - chúng không bao giờ chạm vào khối lập phương được gấp.",
      "Theo dõi sự định hướng tương đối của ba khuôn mặt cạnh nhau.",
      "Xóa các tùy chọn hiển thị sự kết hợp màu không thể được.",
    ],
  ),
  "d2_attention": (
    objective: "Tìm và chọn tất cả các trường hợp của chữ 'd' có chính xác hai dấu gạch ngang.",
    controls: "Đánh đập các miếng đá để chọn hoặc hủy bỏ chúng, sau đó bấm nút SUBMIT khi bạn đã tìm thấy tất cả các mục tiêu.",
    walkthrough: [
      "Quét lưới 4x4 chữ cái (d' và 'p').",
      "Xác định chữ 'd' có chính xác hai dấu gạch ngang (hoặc 2 trên, 2 dưới, hoặc 1 ở trên và 1 ở dưới).",
      "Nhấn phím 'd' để làm nổi bật chúng.",
      "Bỏ qua tất cả các phím 'p' và'd với 1, 3, hoặc 4 dấu gạch ngang.",
      "Xin gõ cửa phòng thí nghiệm để kiểm tra câu trả lời và tiến lên.",
    ],
    strategies: [
      "Quét hàng hoặc cột theo hàng để tránh mục tiêu bị mất.",
      "Nhanh chóng bỏ qua bất kỳ chữ cái 'p' nào mà không đếm dấu gạch ngang của họ.",
      "Đếm tổng gạch ngang trên 'd' cẩn thận, không bị phân tâm bởi vị trí của dấu gạch ngang.",
    ],
  ),
  "definition_dash": (
    objective: "Khớp từ vựng hiển thị với định nghĩa chính xác của nó.",
    controls: "Gõ vào nút định nghĩa tương ứng với ý nghĩa của từ cho đi.",
    walkthrough: [
      "Đọc từ đích được hiển thị trong hộp lớn màu.",
      "Đọc bốn lựa chọn được cung cấp bên dưới.",
      "Chọn định nghĩa đúng phù hợp với từ.",
      "Nếu đúng, bạn sẽ tiến bộ; nếu không đúng, trò chơi sẽ kết thúc.",
    ],
    strategies: [
      "Dùng từ gốc và tiền tố để suy ra ý nghĩa của những từ xa lạ.",
      "Hiển nhiên là loại bỏ những định nghĩa sai lầm trước tiên để thu hẹp lựa chọn của bạn.",
      "Chú ý đến một phần của lời nói (noun, động từ, tính từ) để phù hợp với kiểu định nghĩa.",
    ],
  ),
  "delayed_match_sample": (
    objective: "Hãy nhớ mẫu hoặc hình ảnh mục tiêu, chờ đợi một thời gian trễ, rồi nhận diện nó giữa những người đánh lạc hướng.",
    controls: "Theo dõi mẫu, đợi đến khi kết thúc trễ, và gõ tùy chọn khớp.",
    walkthrough: [
      "Một hình ảnh hoặc mẫu sẽ được hiển thị ngắn trên màn hình.",
      "Màn hình sẽ trống hoặc hiển thị một sự phân tâm trong một thời gian trễ.",
      "Một vài tùy chọn sẽ xuất hiện.",
      "Gõ tùy chọn khớp hoàn hảo với mẫu gốc.",
    ],
    strategies: [
      "Tập trung vào những đặc điểm hoặc màu riêng biệt trong mẫu thay vì toàn bộ hình.",
      "Hãy nhắc lại những đặc điểm thị giác trong thời gian trì hoãn.",
      "Đừng để màn hình trống phá vỡ sự tập trung của bạn.",
    ],
  ),
  "digit_span_reverse": (
    objective: "Hãy nhớ một chuỗi số và nhập chúng theo thứ tự đảo ngược.",
    controls: "Xem các chữ số xuất hiện, sau đó sử dụng bàn phím trên màn hình để nhập ngược lại.",
    walkthrough: [
      "Xem chuỗi số được hiển thị từng số một.",
      "Chờ cho trình tự hoàn thành.",
      "Dùng bàn phím để nhập các chữ số vào đúng thứ tự đảo ngược.",
      "Hãy đưa ra câu trả lời để xem bạn có đúng không và tiếp tục đi đến những chuỗi dài hơn không.",
    ],
    strategies: [
      "Tập hợp các con số thành từng cặp hoặc ba lần khi chúng xuất hiện để giúp đỡ bộ nhớ.",
      "Tập trung tinh thần về phía sau như được trình bày.",
      "Tập trung mạnh mẽ vào con số cuối cùng được hiển thị, vì nó sẽ là đầu vào đầu vào đầu vào đầu tiên của bạn.",
    ],
  ),
  "digit_swap_eq": (
    objective: "Sửa chữa một phương trình toán học sai bằng cách trao đổi hai số.",
    controls: "Đánh hai chữ số để đổi vị trí và biến phương trình thành sự thật.",
    walkthrough: [
      "Xem xét phương trình sai được trình bày.",
      "Tính kết quả hiện tại của hai bên trái và phải.",
      "Xác định hai số nào, khi trao đổi, sẽ cân bằng phương trình.",
      "Gõ chữ số đầu tiên, sau đó gõ số thứ hai để thực hiện trao đổi.",
    ],
    strategies: [
      "Hãy tìm sự khác biệt giữa hai bên để ước lượng những gì cần phải thay đổi.",
      "Tập trung vào những con số có tác động lớn nhất (v.g., mười số tương ứng với những số).",
      "Kiểm tra các hoạt động, trao đổi số trong một phần nhân thay đổi nghiêm trọng giá trị.",
    ],
  ),
  "directions_recall": (
    objective: "Ghi nhớ một chuỗi các mũi tên hướng và sao chép chuỗi.",
    controls: "Xem các mũi tên xuất hiện, sau đó gõ các nút điều hướng tương ứng theo thứ tự chính xác.",
    walkthrough: [
      "Theo dõi chuỗi mũi tên (lên, xuống, trái, phải) được hiển thị trên màn hình.",
      "Đợi chuỗi cần hoàn tất hiển thị.",
      "Gõ các nút điều hướng để nhập chính xác chuỗi từ bộ nhớ.",
      "Hoàn tất trình tự đúng cách để tiến tới những vòng quay dài hơn.",
    ],
    strategies: [
      "Gán từ (ví dụ, North, Nam, Đông, Tây) cho mũi tên nếu bộ nhớ bằng miệng dễ dàng hơn.",
      "Hãy hình dung trình tự như một đường đi xuyên qua không gian.",
      "Chui mũi tên thành nhóm 3 hoặc 4.",
    ],
  ),
  "distractor_matrix": (
    objective: "Xác định các hình ảnh/ đường dẫn cụ thể được ẩn giữa các thiết bị đánh lạc hướng tương tự.",
    controls: "Ghi lại tất cả các ký hiệu mục tiêu trong ma trận.",
    walkthrough: [
      "Lưu ý biểu tượng mục tiêu được hiển thị ở đầu vòng.",
      "Quét lưới biểu tượng dày đặc.",
      "Theo dõi từng trường hợp biểu tượng mục tiêu.",
      "Tránh đánh lạc hướng, rồi điền câu trả lời.",
    ],
    strategies: [
      "Tìm tính năng xác định làm phân biệt mục tiêu với kẻ đánh lạc hướng.",
      "Kiểm tra các mạng lưới theo kiểu, hàng dọc.",
      "Hãy dành thời gian, sự chính xác còn quan trọng hơn tốc độ để tránh hình phạt.",
    ],
  ),
  "divided_attention": (
    objective: "Thực hiện hai nhiệm vụ khác nhau cùng một lúc mà không để thất bại.",
    controls: "Dùng điều khiển bên trái cho một nhiệm vụ và điều khiển bên phải cho bên kia.",
    walkthrough: [
      "Hiểu yêu cầu của Tác vụ A (ví dụ, sắp xếp các hình).",
      "Hiểu các đòi hỏi của Tác vụ B (ví dụ, tránh trở ngại).",
      "Theo dõi liên tục cả hai bên của màn hình.",
      "Phản ứng với kích thích ở cả hai bên để tiếp tục trò chơi.",
    ],
    strategies: [
      "Đừng chú tâm vào một bên của màn hình; hãy giữ mắt bạn di chuyển qua lại.",
      "Ưu tiên công việc mà tình trạng thất bại sắp xảy ra.",
      "Dựa vào thị lực ngoại biên để phát hiện chuyển động hay thay đổi.",
    ],
  ),
  "divisibility_dash": (
    objective: "Xác định con số chia hết cho một số mục tiêu đã cho trong giới hạn thời gian.",
    controls: "Hãy gõ những con số đang rơi xuống hoặc xuất hiện những con số được chia hết bởi mục tiêu.",
    walkthrough: [
      "Chú ý bộ xem thử đích được hiển thị ở đầu màn hình.",
      "Xem các con số trên bảng.",
      "Nhanh chóng thực hiện sự phân chia tâm thần.",
      "Chỉ gõ số chia đều cho mục tiêu.",
    ],
    strategies: [
      "Ghi nhớ các quy tắc xác thực (ví dụ, kết thúc trong 0/ 5 cho 5, tổng số chữ số cho 3 và 9).",
      "Bỏ qua những câu trả lời rõ ràng (ví dụ, số lẻ cho một người ngay cả divitor).",
      "Tập trung vào độ chính xác trước, tốc độ sẽ theo sau.",
    ],
  ),
  "dnms": (
    objective: "Hãy chọn đối tượng tiểu thuyết đã không được hiển thị trong mẫu trước. Điểm số 12 hay nhiều hơn để giành chiến thắng.",
    controls: "Hãy quan sát mẫu, chờ đợi, rồi vỗ vào vật thể mới/ khác biệt.",
    walkthrough: [
      "Xem mẫu vật được hiển thị trên màn hình.",
      "Chờ màn hình dọn dẹp trong thời gian trễ.",
      "sẽ xuất hiện nhiều vật thể, chỉ có một vật thể mới là vật thể mới.",
      "Gõ vào vật thể trong tiểu thuyết khác với biểu tượng và màu sắc so với mẫu.",
    ],
    strategies: [
      "Hãy khóa chặt cả biểu tượng và màu sắc của đối tượng mẫu trong tâm trí bạn.",
      "Thẻ chính xác là thẻ hoàn toàn khác ( biểu tượng khác nhau và màu khác nhau).",
      "Những lá bài có cùng biểu tượng hay cùng màu với mẫu là mồi nhử.",
      "Sự gia tăng khó khăn với những đường nét đúng: càng nhiều mồi nhử xuất hiện khi bạn thành công.",
    ],
  ),
  "dominosa": (
    objective: "Xây dựng lại một tập hợp quân cờ bằng cách ghép những con số gần nhau trên một mạng lưới.",
    controls: "Gõ và kéo giữa các số kề nhau để tạo thành một đô- mi-nô.",
    walkthrough: [
      "nhìn vào lưới số.",
      "Xác định cặp số kề nhau hợp lệ.",
      "Tap và kéo theo nhóm hai số.",
      "Bao phủ toàn bộ lưới chính xác một lần mà không có độ đôminô chồng chéo.",
    ],
    strategies: [
      "Tìm những cặp mà chỉ có thể được tạo ra ở một nơi cụ thể.",
      "Làm việc từ các cạnh và góc bên trong.",
      "Theo dõi các quân cờ (ví dụ, 2-3, 4-4) bạn đã đặt rồi.",
    ],
  ),
  "double_n_back": (
    objective: "Đồng thời theo dõi thính giác và kích thích thị giác, chỉ ra khi nào sự kích thích hiện tại khớp với một trong những từ \"N\" trở lại.",
    controls: "Nhấn nút « Ghi chú » hay « Khớp » khi thích hợp.",
    walkthrough: [
      "Ghi chú mức N hiện tại (ví dụ, N = 2 có nghĩa là so sánh với 2 bước trước).",
      "Một chuỗi các ô vuông sẽ xuất hiện ở các vị trí khác nhau trong khi các chữ cái được phát âm.",
      "Nếu quảng trường ở cùng vị trí với N bước trước, tap Match.",
      "Nếu lá thư được nghe thấy giống như N bước trước, tap Match.",
    ],
    strategies: [
      "Đừng cố nhớ toàn bộ chuỗi; hãy thường xuyên cập nhật bộ nhớ của bạn.",
      "Nói lớn tiếng chữ cái trong khi hình dung vị trí mạng lưới.",
      "Thực hiện một N-back nhiệm vụ nếu hai lần theo dõi là quá khó.",
    ],
  ),
  "double_trouble": (
    objective: "Quản lý hai trò chơi nhỏ đồng thời bằng cách gõ mục tiêu ở cả hai mặt của màn hình.",
    controls: "Đập những quả táo rơi bên trái và những quả bóng đang lớn bên phải.",
    walkthrough: [
      "Ở bên trái, ta gõ táo xanh để ghi điểm trước khi chạm đáy.",
      "Tránh lọc táo đỏ khi trừ điểm.",
      "Bên phải, vỗ vào bong bóng xanh trước khi nó quá lớn và nổ tung.",
      "đạt được số lần gõ xuyên qua cả hai bên để hoàn thành trò chơi.",
    ],
    strategies: [
      "Giữ mắt di chuyển giữa hai bên để tránh bị mất mục tiêu.",
      "Ưu tiên việc bắt táo xanh nhanh chóng, vì việc bỏ lỡ chúng cũng tốn kém.",
      "Các bong bóng nổ sớm trước khi chúng đến quá gần để tự nổ tung.",
    ],
  ),
  "dual_coding": (
    objective: "Ghi nhớ những cặp hình ảnh và từ ngữ miêu tả khác nhau.",
    controls: "Nghiên cứu các cặp, sau đó chọn chính xác từ hoặc hình ảnh phù hợp trong giai đoạn thử nghiệm.",
    walkthrough: [
      "một chuỗi các cặp từ hình ảnh sẽ được trình bày.",
      "Tập trung vào việc tạo mối liên kết giữa hình và từ.",
      "Trong giai đoạn thử, một hình ảnh hoặc một từ sẽ được hiển thị.",
      "Chọn cặp tương ứng từ các tùy chọn cho.",
    ],
    strategies: [
      "Tạo ra những câu chuyện tinh thần sống động, kỳ lạ hay buồn cười kết hợp từ ngữ và hình ảnh.",
      "Hãy tập trung vào những đặc điểm cụ thể của ảnh và liên kết chúng với âm tiết của từ.",
      "Tập luyện lại các mối quan hệ như vẻ ngoài của chúng.",
    ],
  ),
  "dual_mirror": (
    objective: "Điều khiển hai đối tượng di chuyển theo hai hướng ngược lại để đạt được mục tiêu của mỗi mục tiêu.",
    controls: "Cắt hoặc kéo để di chuyển. Một đối tượng theo ngón tay, còn lại di chuyển ngược lại.",
    walkthrough: [
      "Xác định con trỏ chính và con trỏ đã phản chiếu.",
      "Xác định vị trí mục tiêu.",
      "Kéo con chạy chính. Con trỏ đã phản chiếu sẽ di chuyển theo hướng ngược lại.",
      "Di chuyển xung quanh các chướng ngại vật để đặt cả hai con trỏ trong vùng mục tiêu cùng một lúc.",
    ],
    strategies: [
      "Chủ yếu tập trung vào con chạy gần gũi nhất với chướng ngại vật hoặc tường thành.",
      "Di chuyển chậm; chuyển động nhanh có thể làm con chạy đã phản chiếu sụp đổ.",
      "Dùng bức tường để \"làm dấu\" con trỏ bằng cách cố tình va vào tường trong khi người kia di chuyển.",
    ],
  ),
  "dual_task_memory": (
    objective: "Ghi nhớ một bộ đồ vật đồng thời thực hiện một nhiệm vụ thứ hai gây phân tâm.",
    controls: "Nghiên cứu vật dụng, tương tác với công việc phân tâm bằng cách gõ vào, rồi nhớ lại những vật đầu tiên.",
    walkthrough: [
      "Ghi nhớ chuỗi hoặc tập hợp mục tiêu được hiển thị.",
      "Hoàn thành công việc phân tâm hoạt động (ví dụ giải toán đơn giản hoặc gõ các vật thể di chuyển).",
      "Một khi nhiệm vụ đánh lạc hướng kết thúc, hãy nhớ và nhập mục tiêu gốc.",
      "Hãy đưa ra câu trả lời.",
    ],
    strategies: [
      "Hợp nhất các mục tiêu bộ nhớ trước khi nhiệm vụ đánh lạc hướng bắt đầu.",
      "Tập trung tinh thần những mục tiêu ở phía sau trong khi thực hiện nhiệm vụ đánh lạc hướng.",
      "Đừng quá chú tâm vào công việc của người phân tâm; hãy chú ý đến công việc đó.",
    ],
  ),
  "dynamic_salience": (
    objective: "Theo dõi các mục tiêu cụ thể khi chúng di chuyển giữa các thiết bị đánh lạc hướng tương tự.",
    controls: "Nhìn mục tiêu di chuyển, rồi vỗ chúng khi chúng dừng lại.",
    walkthrough: [
      "Lúc đầu, một số mục sẽ chiếu nhanh hoặc làm nổi bật mục tiêu của bạn.",
      "Mọi mục sẽ trở nên giống hệt nhau và bắt đầu di chuyển xung quanh màn hình.",
      "Theo dõi chuyển động của mục tiêu cụ thể.",
      "Khi chuyển động dừng lại, hãy gõ các mục bạn theo dõi.",
    ],
    strategies: [
      "Hãy thử xem mục tiêu là hình di chuyển đơn (ví dụ một hình tam giác nếu có 3 mục tiêu).",
      "Đừng nhìn thẳng vào một mục tiêu; hãy tập trung mắt vào trung tâm của nhóm.",
      "Tránh chớp mắt khi các vật dụng đang chuyển động.",
    ],
  ),
  "einstein_riddle": (
    objective: "Sử dụng một tập hợp các manh mối để suy luận các thuộc tính thuộc các đối tượng khác nhau trên một mạng lưới.",
    controls: "Các tế bào lưới đập để đánh dấu chúng là đúng (đánh dấu) hay sai dựa trên các manh mối.",
    walkthrough: [
      "Đọc danh sách những manh mối hợp lý sẵn có.",
      "Các thuộc tính tham chiếu chéo trên mạng logic.",
      "Gõ một tế bào để đánh dấu một giao lộ là đúng (mà tự động vượt qua phần còn lại của hàng/column).",
      "Tiếp tục giảm dần cho đến khi toàn bộ lưới được lấp đầy.",
    ],
    strategies: [
      "Bắt đầu với những manh mối trực tiếp nhất mà rõ ràng liên kết hai mục.",
      "Sử dụng manh mối tiêu cực để loại bỏ các khả năng ngay lập tức.",
      "Tìm phản ứng dây chuyền nơi đặt một dấu check mạnh hơn.",
    ],
  ),
  "etymology_origin": (
    objective: "Hãy xác định nguồn gốc lịch sử chính xác (v.g., La - tinh, Hy Lạp, tiếng Anh cổ) của từ này.",
    controls: "Ấn nút tương ứng với nguồn gốc ngôn ngữ đúng.",
    walkthrough: [
      "Đọc từ vựng đích.",
      "Xem lại các tùy chọn nguồn gốc ngôn ngữ đa ngôn ngữ.",
      "Gõ lại nguồn gốc mà bạn tin rằng từ đó bắt nguồn từ.",
      "hoàn thành hiệp để xem điểm số của bạn.",
    ],
    strategies: [
      "Tìm kiếm các tiền tố và hậu tố chung (ví dụ, 'anti', 'ology' thường chỉ đến tiếng Hy Lạp; 'tion', 'pre' to Latin).",
      "Những từ ngữ đơn giản và đơn giản thường xuất phát từ tiếng Anh và Đức cổ.",
      "Các khái niệm khoa học hoặc trừu tượng thường có nguồn gốc La - tinh hoặc Hy Lạp.",
    ],
  ),
  "etymon_oddball": (
    objective: "Hãy xác định từ trong một danh sách không có cùng gốc địa ngục như những người khác.",
    controls: "Hãy gõ vào từ mà là một lẻ ra.",
    walkthrough: [
      "Xem xét danh sách những từ được cung cấp.",
      "Nhận diện gốc hoặc tiền tố chung của hầu hết các từ.",
      "Tìm từ giống nhau nhưng bắt nguồn từ một nghĩa gốc hoàn toàn khác.",
      "Hãy gõ lại câu trả lời.",
    ],
    strategies: [
      "Tập trung vào ý nghĩa của từ ngữ, không chỉ đánh vần.",
      "Hãy coi chừng những từ có gốc điệu đồng tính (âm thanh giống nhau nhưng có ý nghĩa khác nhau).",
      "Nếu không chắc chắn, tìm kiếm từ không phù hợp với chủ đề ngữ nghĩa tổng thể của nhóm.",
    ],
  ),
  "event_timeline_memory": (
    objective: "Hãy nhớ lại một chuỗi các biến cố lịch sử hoặc tưởng tượng và ngày tháng của chúng, rồi sắp xếp theo thứ tự thời gian.",
    controls: "Kéo và thả thẻ sự kiện vào đúng thời gian.",
    walkthrough: [
      "Xem xét danh sách các sự kiện và ngày tháng hoặc nhãn thời gian tương ứng.",
      "Một khi giai đoạn học kết thúc, các sự kiện sẽ bị xáo trộn và ngày tháng bị che khuất.",
      "Kéo các sự kiện lên và xuống để sắp xếp từ sớm nhất cho đến mới nhất.",
      "Chuyển đổi dòng thời gian để kiểm tra độ chính xác của bạn.",
    ],
    strategies: [
      "Tạo ra một câu chuyện tinh thần kết nối các sự kiện theo thứ tự mà họ đã xảy ra.",
      "Hãy tập trung vào những biến cố đầu tiên và cuối cùng mà trí nhớ bạn nhớ chắc chắn.",
      "Tìm những mối quan hệ hợp lý giữa các sự kiện.",
    ],
  ),
  "face_name_association": (
    objective: "Hãy nhớ những cái tên liên quan đến những khuôn mặt khác nhau và nhớ lại chúng trong giai đoạn thử nghiệm.",
    controls: "Học tên và khuôn mặt, rồi gõ hoặc chọn đúng tên khi có mặt.",
    walkthrough: [
      "Một loạt khuôn mặt sẽ được thể hiện, mỗi cặp có một tên.",
      "Hãy nhớ sự kết hợp giữa các nét mặt và tên.",
      "Trong giai đoạn thử nghiệm, một khuôn mặt sẽ được trình bày mà không có tên.",
      "Chọn hoặc nhập tên đúng tương ứng với khuôn mặt đó.",
    ],
    strategies: [
      "Tìm một nét đặc trưng trên mặt (v.g., mũi nổi bật, tóc đặc biệt) và liên kết nó với tên.",
      "Nếu tên là \"Smith\", hãy tưởng tượng một cái búa thợ rèn đập vào nét mặt nổi bật nhất của chúng.",
      "Nhắc lại tên trong khi nhìn chằm chằm vào mặt.",
    ],
  ),
  "face_trait_association": (
    objective: "Ghi nhớ những đặc điểm cá nhân (v.g., nghề nghiệp, sở thích) liên quan đến những gương mặt khác nhau.",
    controls: "Học những khuôn mặt và tính cách, rồi chọn đúng tính cách khi bị thử thách.",
    walkthrough: [
      "Mặt đối mặt với những đặc điểm hoặc sự kiện cụ thể.",
      "Hãy nhớ đặc điểm nào thuộc về người đó.",
      "Trong giai đoạn thử nghiệm, một khuôn mặt sẽ xuất hiện với nhiều lựa chọn tính cách khác nhau.",
      "Gõ đúng tính cách được kết hợp với khuôn mặt ban đầu.",
    ],
    strategies: [
      "Hãy hình dung một người tích cực tham gia vào tính cách hoặc nghề nghiệp của mình.",
      "Hãy tạo ra một câu chuyện nhanh chóng, đáng nhớ về lý do tại sao người đó có đặc điểm đó dựa trên cách nhìn của họ.",
      "Nhóm đối mặt với những đặc điểm tương tự nếu có thể giảm tải bộ nhớ.",
    ],
  ),
  "fact_binder": (
    objective: "Ghi nhớ những tập hợp các dữ kiện liên kết về các đề tài khác nhau và trả lời các câu hỏi về chúng.",
    controls: "Đọc các bài báo thực tế, rồi gõ chính xác các câu trả lời cho các câu hỏi trắc nghiệm.",
    walkthrough: [
      "Nghiên cứu thông tin được trình bày bao gồm nhiều sự kiện liên quan đến đề tài chính.",
      "Hãy cố gắng xây dựng một mô hình tinh thần toàn diện về các thông tin này.",
      "Sau giai đoạn học, hãy đọc những câu hỏi thử trí nhớ của bạn.",
      "Chọn câu trả lời đúng dựa trên những sự kiện bạn nhớ.",
    ],
    strategies: [
      "Hãy sắp xếp các sự kiện thành phân loại (ví dụ, ngày tháng, địa điểm, tên).",
      "Cố gắng xác định mối liên hệ hợp lý giữa các sự kiện khác nhau.",
      "Đừng chỉ đọc thụ động; hãy tích cực tự kiểm tra khi học.",
    ],
  ),
  "factor_finder": (
    objective: "Xác định tất cả các yếu tố chính hoặc yếu tố thường xuyên của một số mục tiêu cho trước.",
    controls: "Đập vào chính xác số bong bóng là yếu tố của mục tiêu.",
    walkthrough: [
      "Xem số mục tiêu lớn hiển thị trên màn hình.",
      "Xem lại các tùy chọn nổi hoặc các lựa chọn dựa trên mạng lưới.",
      "Gõ tất cả các con số có thể là yếu tố chính đáng (đi thẳng vào mục tiêu).",
      "Tránh khai thác con số không phải là yếu tố để ngăn chặn những điểm đánh mất.",
    ],
    strategies: [
      "Bắt đầu với các yếu tố dễ nhất: 2 (nếu ngay cả), 3 (nếu tổng số chữ số chia hết cho 3) và 5.",
      "Hãy nhớ rằng các yếu tố thường đi theo cặp (v.g., nếu 2 là một yếu tố của 24, thì đó là 12).",
      "Làm việc có hệ thống từ nhỏ nhất đến lớn nhất.",
    ],
  ),
  "feature_matrix_recall": (
    objective: "Ghi nhớ một lưới chứa biểu tượng với các tính năng cụ thể (color, hình, mẫu) và tái tạo nó.",
    controls: "Nghiên cứu lưới điện, rồi tái thiết nó bằng cách chọn đúng các đặc điểm cho mỗi ô trống.",
    walkthrough: [
      "Một ma trận chứa các biểu tượng phức tạp (thay đổi hình, màu và mẫu) được hiển thị.",
      "Hãy nhớ chính xác vị trí và đặc điểm của mỗi biểu tượng.",
      "Ma trận sẽ rõ ràng, để lại những ô trống.",
      "Xây dựng lại ma trận bằng cách đặt các biểu tượng chính xác trở lại các tế bào ban đầu.",
    ],
    strategies: [
      "Tìm mẫu trong lưới (ví dụ, tất cả các mục màu đỏ trong một hàng, tất cả các vòng tròn trong cùng một cột).",
      "Lấy ma trận thành các phần nhỏ hơn (ví dụ, 2x2 block) thay vì học thuộc lòng từng tế bào.",
      "Ưu tiên việc nhớ một tính năng trước (như hình) và trí óc tô màu ở trên.",
    ],
  ),
  "fibonacci_merge": (
    objective: "Trượt trên một mạng lưới để hợp nhất các con số Fibonacci liên tiếp và đạt đến con số cao nhất có thể.",
    controls: "Cuộn lên, xuống, trái, hoặc phải để di chuyển tất cả các gạch theo hướng đó.",
    walkthrough: [
      "Đánh sập lưới để di chuyển mọi đá lát theo hướng đã chọn.",
      "Khi hai số Fibonacci liên tiếp (v.g., 2 và 3, hoặc 5 và 8) va chạm nhau, chúng hợp nhất thành số Fibonacci kế tiếp (v.g., 5, 13).",
      "Ghi chú rằng 1 có thể kết hợp với 1 khác để làm 2.",
      "Tiếp tục trộn các mảnh để giải phóng không gian và xây dựng số lượng lớn hơn trước khi lưới được lấp đầy.",
    ],
    strategies: [
      "Giữ ô vuông giá trị cao nhất của bạn ở một góc nhất định của lưới.",
      "Chỉ lấy hai hoặc ba hướng (ví dụ, Down and Right) để duy trì tổ chức.",
      "Hãy lên kế hoạch những bước tiếp theo để mang những con số liên tiếp kề nhau.",
    ],
  ),
  "fillomino": (
    objective: "Chia lưới thành các đa giác với kích cỡ khớp. Hai đa giác cùng kích cỡ không thể chạm vào cùng cạnh.",
    controls: "Các tế bào đập để chu kỳ qua các con số từ 1 đến 9.",
    walkthrough: [
      "Kiểm tra các số bắt đầu trên mạng lưới.",
      "Mỗi số tượng trưng cho kích thước của khối (polyomino) nó thuộc về.",
      "Gõ bên cạnh các tế bào để chỉ định cùng một số để nhóm chúng lại.",
      "Bảo đảm không có hai khối nào cùng cỡ với nhau có cạnh ngang hay dọc.",
      "Điền tất cả các tế bào lưới để giải câu đố.",
    ],
    strategies: [
      "Bắt đầu với những con số nhỏ như 1, ngay lập tức là những khối biệt lập.",
      "Tìm những con đường buộc phải mở rộng bởi vì chúng không thể kết hợp với những nhóm có cùng kích thước.",
      "Theo dõi kích cỡ khối bằng cách đếm các tế bào với cùng số lượng.",
    ],
  ),
  "find_word": (
    objective: "Xác định từ mục tiêu trong một mạng lưới chữ cái bị xáo trộn.",
    controls: "Kéo ngang các chữ cái, dọc hoặc chéo nhau để đánh vần chữ.",
    walkthrough: [
      "Xem từ đích được hiển thị ở đầu trang.",
      "Quét lưới để tìm chữ bắt đầu.",
      "Kéo ngón tay qua những chữ kế nhau để làm nổi bật từ đầy đủ.",
      "Thả ngón tay ra để phục hồi sự lựa chọn.",
    ],
    strategies: [
      "Trước tiên, hãy tìm hai chữ cái hoặc phụ âm độc đáo (như Z, K, X).",
      "Tìm kiếm mạng lưới một cách có hệ thống bắt đầu từ phía trên bên trái.",
      "Kiểm tra hướng của từ (sau, lùi, chéo) trước khi kéo.",
    ],
  ),
  "flanker_test": (
    objective: "Hãy nhanh chóng nhận ra hướng của mũi tên trung tâm, đồng thời lờ đi những mũi tên bên hông.",
    controls: "Ấn nút trái hay phải tùy thuộc vào hướng mũi tên trung tâm.",
    walkthrough: [
      "Một hàng mũi tên xuất hiện trên màn hình (ví dụ g., <<><<>.",
      "Chỉ tập trung vào mũi tên trung tâm (phần giữa).",
      "Bỏ qua các mũi tên xung quanh (không đối xứng hoặc không đồng nhất).",
      "Nhấn nút điều khiển càng nhanh càng tốt.",
    ],
    strategies: [
      "Nhắm mắt vào trung tâm của màn hình trước thời gian.",
      "Thở và phản ứng với chỉ hướng hình ảnh của mũi tên giữa.",
      "Đừng để những kẻ tấn công tay sai lừa bạn vào nhầm bên.",
    ],
  ),
  "focus_tunnel": (
    objective: "Theo dõi và theo một mục tiêu khi nó di chuyển qua một đường hầm thị giác phức tạp.",
    controls: "Dùng cần điều khiển để lái và theo dõi đối tượng.",
    walkthrough: [
      "Xem mục tiêu được tô sáng lúc đầu.",
      "Đi theo vật thể khi nó đi sâu hơn vào đường hầm.",
      "Di chuyển hoặc nhìn vào hướng mà vật thể đang di chuyển.",
      "Tiếp tục theo dõi chính xác để giữ sự tập trung.",
    ],
    strategies: [
      "Hãy thư giãn đôi mắt của bạn để đi trên con đường rộng hơn phía trước.",
      "Dự đoán sẽ rẽ vào đường hầm dựa trên quỹ đạo của vật thể.",
      "Bỏ qua việc đánh lạc hướng hình ảnh bên trong đường hầm.",
    ],
  ),
  "fraction_match": (
    objective: "Khớp các phân số tương đương hoặc khớp các giá trị phân số với hình ảnh của chúng.",
    controls: "Đánh dấu phân số tương ứng hoặc thả chúng vào các khe cắm khớp.",
    walkthrough: [
      "Hãy xem hình nhỏ được hiển thị (bánh hoặc số điện thoại).",
      "Tìm thẻ tương ứng với giá trị tương đương (ví dụ, 2/ 4 khớp 1/2).",
      "Gõ hoặc kéo để kết nối chúng.",
      "Khớp chính xác tất cả thẻ để hoàn thành cấp độ.",
    ],
    strategies: [
      "Đơn giản hóa phân số thành những từ thấp nhất ngay lập tức.",
      "Để có bánh hình ảnh, hãy đếm tổng số đoạn đầu tiên (deominator) rồi sau đó đánh bóng các bộ phận (số).",
      "Thực hành sự cải đạo phân số thông thường (tiếng súng, phần tư, phần ba).",
    ],
  ),
  "fraction_matcher": (
    objective: "Tìm các biểu hiện tương đương của phân số.",
    controls: "Đập bài tương đương phân số để ghép chúng lại.",
    walkthrough: [
      "Kiểm tra các quân bài chứa các con số, hình dạng hoặc biểu tượng.",
      "Tính giá trị phân số của mỗi bước.",
      "Chọn những cặp đại diện cho cùng giá trị.",
      "Dọn sạch tất cả các quân cờ để thắng.",
    ],
    strategies: [
      "Tìm kiếm các trận đấu thị giác dễ dàng trước.",
      "Hãy giảm tất cả các con số xuống các dạng phân số đơn giản hóa.",
      "Sử dụng quá trình loại bỏ cho số nhỏ hơn.",
    ],
  ),
  "fractional_pizza": (
    objective: "Phục vụ đúng lượng pizza cắt theo thứ tự phân số.",
    controls: "Gõ để cắt hoặc chọn số lượng yêu cầu của lát pizza.",
    walkthrough: [
      "đọc thứ tự (ví dụ, '1/2 của một pizza 8 chuỗi\" hoặc '3/4 của một pizza 12- giây).",
      "Tính chính xác số lát cần thiết.",
      "Chọn hoặc phục vụ số lát đó.",
      "Hãy ra lệnh thỏa mãn khách hàng.",
    ],
    strategies: [
      "Nhân phân số với tổng số lát.",
      "Hãy hình dung một nửa hay một phần tư của pizza để ước lượng nhanh.",
      "Kiểm tra toán trước khi thi đấu để tránh mất điểm.",
    ],
  ),
  "frequency_tap": (
    objective: "So sánh tỷ lệ xung của hai tấm đèn và xác định cái nào khớp với tần số mục tiêu (ví dụ, 1.5Hz).",
    controls: "Gõ vào bảng điều khiển trái hoặc phải tương ứng với tần số chính xác.",
    walkthrough: [
      "Đọc tần số mục tiêu ở đầu màn hình.",
      "Theo dõi tốc độ đập nhanh của bảng \"A\" và \"B\".",
      "Nhấn vào bảng điều khiển xung quanh tần số mục tiêu.",
      "Hãy trả lời đúng cách để gia tăng điểm số trước khi thời gian trôi qua.",
    ],
    strategies: [
      "Sử dụng tần số tham chiếu là một đường cơ bản (ví dụ, 1.0Hz là một xung trên giây).",
      "xung tần số cao hơn nhanh hơn, xung tần số thấp hơn chậm hơn.",
      "Dựa vào nhịp điệu thị giác thay vì đếm chính xác phần nghìn giây.",
    ],
  ),
  "futoshiki": (
    objective: "Điền vào lưới với con số để mỗi hàng và cột chứa con số độc nhất vô nhị, trong khi tôn trọng các dấu hiệu bất bình đẳng (<, >) giữa các tế bào.",
    controls: "Hãy gõ vào một tế bào để chọn nó, rồi dùng numpad ở phía dưới để nhập một số. Hãy dùng cái nút xóa để xoá sạch một ô.",
    walkthrough: [
      "Tìm dấu hiệu bất bình đẳng giữa các tế bào lân cận.",
      "Tìm hàng hoặc cột với số còn thiếu và dùng các dấu hiệu để suy ra các giá trị.",
      "Gõ vào một ô trống và chọn đúng số ở hàng dưới.",
      "Hoàn thành lưới mà không vi phạm bất bình đẳng hay sự độc đáo hàng/column.",
    ],
    strategies: [
      "Hãy tìm chuỗi số bất bình đẳng (v.g., A < B < C) hạn chế nghiêm trọng các con số có thể.",
      "Xác định những con số cao nhất và thấp nhất có thể trong lưới để điền vào các cạnh của sự bất bình đẳng.",
      "Sử dụng quá trình loại bỏ theo hàng và cột như bạn sẽ làm ở Sudoku.",
    ],
  ),
  "game_2048": (
    objective: "Kết hợp các miếng gạch với các con số tương tự để đạt tới 2048 lát gạch.",
    controls: "Kéo lên, xuống, trái, hoặc phải bất cứ nơi nào trên màn hình để trượt tất cả các mảnh theo hướng đó.",
    walkthrough: [
      "Chuyển tất cả các miếng theo một hướng.",
      "Khi hai mảnh với cùng số chạm nhau, chúng hợp nhất thành một viên gạch với giá trị gấp đôi.",
      "Sau mỗi lần cạo, có 2 hay 4 ô vuông mới xuất hiện trên bảng.",
      "Tiếp tục kết hợp các mảnh để giải phóng không gian và xây dựng hướng tới 2048.",
    ],
    strategies: [
      "Giữ những miếng gạch có giá trị cao nhất ở một góc.",
      "Hãy hạn chế việc đi theo ba hướng chủ yếu để duy trì chiến lược ở góc.",
      "Cố gắng tổ chức những miếng gạch của bạn trong một chuỗi giảm dần để cho phép làm tan chảy sự hợp nhất.",
    ],
  ),
  "gear_rotation": (
    objective: "Xác định hướng quay của bánh răng cuối cùng theo một trình tự, theo hướng của bánh số bắt đầu.",
    controls: "Gõ vào nút 'CLLWISE' hay 'CARER-CLLLWISE'.",
    walkthrough: [
      "Quan sát chuỗi các bánh răng liên kết.",
      "Lưu ý hướng quay của bánh số đầu tiên (được đánh dấu bởi mũi tên).",
      "Theo dõi vòng quay qua chuỗi, nhớ rằng các bánh răng bên cạnh quay theo hướng ngược lại.",
      "Chọn hướng xoay đúng cho thiết bị cuối.",
    ],
    strategies: [
      "Các thiết bị điều hướng luôn quay theo hướng ngược lại.",
      "Nếu có một số bánh răng lẻ trong chuỗi, các bánh răng đầu và cuối quay theo cùng một hướng.",
      "Nếu có một số bánh răng chẵn, bánh răng đầu và cuối quay theo hướng ngược lại.",
    ],
  ),
  "ghost_tap": (
    objective: "Mở màn hình chính xác vào lúc này, một cái tháp ra-đa vô hình có tần số cao nhất.",
    controls: "Đập bất cứ chỗ nào trên màn hình.",
    walkthrough: [
      "Xem vòng tròn nghiền nát mở rộng và co lại.",
      "Hãy nội bộ nhịp đập trong vài chu kỳ đầu tiên.",
      "Khi xung trở nên vô hình (Ghost mode), tiếp tục theo dõi nhịp điệu trong đầu.",
      "Mở màn hình chính xác khi nào những xung điện vô hình sẽ đạt đến đỉnh điểm.",
    ],
    strategies: [
      "Đếm cùng với các xung thị giác để thiết lập một nhịp tim ổn định bên trong.",
      "Đừng vội vỗ của bạn, hãy tin tưởng giai điệu bạn thiết lập trong giai đoạn nhìn thấy được.",
      "Nếu bạn là một chút tắt, điều chỉnh thời gian của bạn cho vòng tiếp theo dựa trên phản hồi.",
    ],
  ),
  "gokigen_naname": (
    objective: "Vẽ một đường chéo trong mỗi tế bào để các đường thẳng gặp nhau ở mỗi ngã tư khớp với đầu mối số, mà không tạo ra bất kỳ vòng khép kín nào.",
    controls: "Hãy gõ vào một tế bào để lật ngược hướng của đường chéo của nó (ra dấu gạch lát hoặc gạch sau).",
    walkthrough: [
      "nhìn vào các vòng tròn đánh số tại các giao lộ mạng lưới.",
      "Một số chỉ ra chính xác bao nhiêu đường chéo phải kết nối với vòng tròn đó.",
      "Các tế bào đập để vẽ đường chéo, đảm bảo chúng thỏa mãn tất cả các điểm giao nhau.",
      "Kiểm tra xem dòng của bạn không tạo vòng lặp nào.",
    ],
    strategies: [
      "Bắt đầu với các góc và cạnh; một '0' hoặc '4' ở giữa, hoặc '0' hoặc '2' trên một cạnh, ép các đường chéo riêng biệt.",
      "Nếu số 1 ở góc, chỉ có một đường có thể kết nối với nó.",
      "Hãy nhớ rằng các vòng thời gian bị cấm; nếu đặt một đường thẳng thì bạn phải dùng đường chéo đối diện.",
    ],
  ),
  "go_no_go": (
    objective: "Nhanh chóng nhấn vào màn hình khi một biểu tượng « Go » xuất hiện, và KHÔNG gõ khi một biểu tượng « Không được » xuất hiện.",
    controls: "Gõ bất cứ chỗ nào trên màn hình là 'Đi'.",
    walkthrough: [
      "Chờ biểu tượng xuất hiện trên màn hình.",
      "Nếu biểu tượng là một dấu « Go » (dấu hiệu xanh/ chơi), hãy gõ nhanh màn hình.",
      "Nếu biểu tượng là một biểu tượng 'Không được' (không có dấu chéo), đừng làm gì và đợi nó biến mất.",
      "Xây đắp điểm số bằng cách phản ứng đúng trước một loạt biểu tượng.",
    ],
    strategies: [
      "Giữ cho ngón tay của bạn lơ lửng gần màn hình nhưng tránh nghỉ ngơi để tránh bị chạm vào.",
      "Chủ yếu là tập trung vào màu hoặc hình dạng để đưa ra quyết định chia phần giây.",
      "Hãy thư giãn; quá khích có thể gây ra sự bắt đầu sai trên biểu tượng 'Không đi'.",
    ],
  ),
  "grammar_police": (
    objective: "Xác định nếu một câu đã hiển thị là đúng ngữ pháp hoặc sai.",
    controls: "Nhấn nút 'CORRECT' hay 'TIẾNG'.",
    walkthrough: [
      "Đọc câu được trình bày trên màn hình một cách cẩn thận.",
      "Tìm lỗi trong tình trạng căng thẳng, thỏa thuận chủ đề, hoặc chính tả.",
      "Tap 'CORRECT' nếu câu không có lỗi.",
      "Bắt 'INCORRECT' nếu bạn phát hiện ra sai ngữ pháp.",
    ],
    strategies: [
      "Hãy đọc lớn tiếng câu này trong đầu; đọc nhầm thường chỉ ra một lỗi lầm.",
      "Hãy đặc biệt chú ý đến điện thoại đồng tính (v.G., của họ/có) và của cải.",
      "Đừng vội vã, bảo đảm bạn đánh giá toàn bộ câu trước khi quyết định.",
    ],
  ),
  "grammar_sort": (
    objective: "Phân loại từ thành phần chính xác của lời nói (noun, Verb, hoặc Adjectiive) trước khi thời gian hết.",
    controls: "Gõ vào nút 'NUN', 'VERB', hoặc 'ADJECTIVE' tương ứng với từ hiển thị.",
    walkthrough: [
      "Xem từ được hiển thị ở giữa màn hình.",
      "Xác định nếu nó đại diện cho một người/ nơi/ thứ (Noun), hành động (Verb), hoặc mô tả (Adjecive).",
      "Gõ vào cái nút xô tương ứng ở dưới.",
      "Nhanh chóng sắp xếp càng nhiều từ càng tốt để bạn có thể ghi điểm.",
    ],
    strategies: [
      "Thử đặt từ vào một câu đơn giản (ví dụ, 'Từ' cho danh từ, 'I [từ] cho động từ,' Xe' cho tính từ.",
      "Giữ ngón tay của bạn gần cả ba nút để giảm thiểu thời gian đi lại.",
      "Tập trung vào sự chính xác trên tốc độ; câu trả lời chính xác liên tiếp thường đạt điểm cao hơn.",
    ],
  ),
  "graph_coordinate_plot": (
    objective: "Giải một phương trình tuyến tính cho một giá trị x cho trước và vẽ kết quả (x, y) điểm trên đồ thị tọa độ.",
    controls: "Mở một vị trí trên mạng để đặt một điểm, sau đó nhấn 'SbMIT bit'.",
    walkthrough: [
      "Đọc phương trình (e.g., y = 2x - 1) và giá trị đích x.",
      "Tính giá trị y tương ứng.",
      "Tìm tọa độ (x, y) trên đồ thị và gõ để đặt điểm.",
      "Kiểm tra lựa chọn của bạn và bấm 'bứt điểm'.",
    ],
    strategies: [
      "Kiểm tra hai lần tính toán trước khi gửi, đặc biệt là với số âm.",
      "Hãy nhớ rằng trục x là ngang và trục y là dọc.",
      "Sử dụng đường dây và nhãn hiệu để đảm bảo rằng bạn đã không bị lỗi cách gõ của bạn bởi một đơn vị.",
    ],
  ),
  "grid_displacement": (
    objective: "Ghi nhớ vị trí của các biểu tượng trong một lưới 3x3, và sau đó xác định hai biểu tượng chuyển đổi nơi nào sau khi lưới được giấu.",
    controls: "Đánh vào hai tế bào chứa các biểu tượng trao đổi.",
    walkthrough: [
      "Nghiên cứu lưới biểu tượng 3x3 trong giai đoạn ghi nhớ.",
      "Khi lưới trống, hãy nhớ hình ảnh của lưới.",
      "Khi các ảnh tượng xuất hiện trở lại, hãy để ý đến hai ảnh tượng ở những vị trí mới.",
      "Bắt cả hai biểu tượng để hoàn thành hiệp.",
    ],
    strategies: [
      "Tập trung vào việc học thuộc lòng các góc hay một hàng dài để giữ trí nhớ của bạn.",
      "Hãy cố gắng tạo ra một câu chuyện hoặc mô hình kết nối các biểu tượng trong đầu bạn.",
      "Hãy tìm những hình ảnh cảm thấy \"ra khỏi vị trí\" trong bản đồ tinh thần của bạn khi chúng xuất hiện lại.",
    ],
  ),
  "grocery_list": (
    objective: "Ghi nhớ danh sách các loại thực phẩm và các loại của chúng, sau đó xác định chính xác loại của một món đồ cụ thể trong giai đoạn thử nghiệm.",
    controls: "Hãy nhấn nút phân loại đúng từ các tùy chọn được cung cấp.",
    walkthrough: [
      "Xem lại danh sách các mục và phân loại trong giai đoạn ghi nhớ.",
      "Tap 'REDY' khi bạn đã thuộc lòng danh sách.",
      "Một mục trong danh sách sẽ được hiển thị.",
      "Nhấn nút phân loại mà mục này thuộc về.",
    ],
    strategies: [
      "Nhóm mục theo phân loại trong tâm trí (ví dụ, hãy nhớ tất cả các mục « Bảo vệ » cùng nhau).",
      "Hãy hình dung những đồ vật nằm ở những lối đi khác nhau của cửa hàng tạp hóa.",
      "Dùng thiết bị ghi nhớ hoặc kết hợp với những thứ khó phân loại hơn.",
    ],
  ),
  "homophone_hunt": (
    objective: "Hãy chọn những âm thanh đồng nhất chính xác (từ âm thanh giống nhau nhưng có ý nghĩa/ điệu bộ khác nhau) để hoàn thành câu.",
    controls: "Ấn nút bằng từ viết đúng.",
    walkthrough: [
      "Đọc câu với từ còn thiếu.",
      "Xem lại các lựa chọn có nhiều lựa chọn, đó là âm thanh đồng tính của nhau.",
      "Xác định chính tả nào phù hợp với ngữ cảnh và ý nghĩa của câu.",
      "Gõ đúng lựa chọn.",
    ],
    strategies: [
      "Sử dụng các đầu mối ngữ cảnh; e.g., 'của họ' hiển thị sở hữu, 'có' chỉ ra một vị trí, 'họ' là 'họ'.",
      "Nếu không chắc chắn, tinh thần sẽ thay thế từng định nghĩa vào câu để xem nó có hợp lý không.",
      "Hãy dành thời gian kiểm tra lại chính tả, vì các từ tương tự nhau.",
    ],
  ),
  "hue_sort": (
    objective: "Làm lại những mảnh màu để tạo thành một đường dốc hoàn hảo, không giới hạn, dùng những viên gạch cố định làm neo.",
    controls: "Gõ một viên để chọn nó, rồi gõ vào một miếng gạch khác để đổi vị trí.",
    walkthrough: [
      "Nhận diện những miếng đã cố định có dấu chấm nhỏ; không thể di chuyển chúng.",
      "Hãy nhìn vào sự khác biệt màu sắc giữa các miếng cố định để hiểu hướng của dốc màu.",
      "Gõ một ô vuông, sau đó gõ một cái khác để trao đổi chúng vào đúng thứ tự dốc.",
      "Tiếp tục trao đổi cho đến khi chuyển đổi màu một cách trơn tru trên toàn hệ thống.",
    ],
    strategies: [
      "Bắt đầu bằng cách sắp xếp các cạnh hoặc góc nối các lát cố định.",
      "Sắp xếp theo một chiều màu cùng một lúc (ví dụ, đưa tất cả các mảnh tối nhất qua một bên).",
      "Nếu một miếng gạch trông hơi \"tắt\", hãy trao đổi nó với một người hàng xóm ngay lập tức để xem sự chuyển tiếp có tiến triển không.",
    ],
  ),
  "inequality_balance_ops": (
    objective: "Đánh giá hai biểu thức toán học và xác định chính xác sự bất bình đẳng hoặc mối quan hệ bình đẳng giữa chúng.",
    controls: "Nhấn nút '<','=', hoặc '>'.",
    walkthrough: [
      "Tính giá trị của biểu thức toán học bên trái.",
      "Tính giá trị của biểu thức bên phải.",
      "Hãy so sánh hai giá trị này.",
      "Gõ '<b> nếu trái nhỏ hơn,'> nếu trái lớn hơn, hoặc '=' nếu chúng bằng.",
    ],
    strategies: [
      "Hãy nhớ thứ tự thao tác (PEMDDDAS/BODMAS): nhân/divide trước khi thêm / phụ.",
      "Đôi khi tính toán chính xác là không cần thiết; ước tính có thể nhanh chóng tiết lộ nếu một bên lớn hơn rất nhiều.",
      "Hãy tìm những thuật ngữ chung của cả hai bên mà có thể bị loại bỏ tinh thần để đơn giản hóa toán học.",
    ],
  ),
  "inequality_dash": (
    objective: "Nhanh chóng xác định mối quan hệ (<, =, >) giữa hai biểu thức toán học đơn giản trước khi thời gian hết.",
    controls: "Nhấn nút '<','=', hoặc '>'.",
    walkthrough: [
      "hãy nhìn vào công thức 'LEFT' và 'Right'.",
      "Nhanh chóng giải quyết cả hai công thức trong đầu.",
      "Gõ dấu hiệu bất bình đẳng thích hợp để so sánh.",
      "Trả lời càng nhiều càng tốt trước khi hết giờ.",
    ],
    strategies: [
      "Ưu tiên tốc độ; sử dụng kỹ thuật đánh giá nếu các con số ở xa nhau.",
      "Làm quen với sự cộng và nhân sự kiện để giảm thời gian tính toán.",
      "Giữ nhịp độ ổn định và cố đừng hoảng sợ khi đồng hồ chạy chậm.",
    ],
  ),
  "interlock_puzzle": (
    objective: "Xác định nếu hai khối ba chiều sẽ phù hợp với nhau hoàn hảo để hình thành một khối rắn/prim.",
    controls: "Kéo lên màn hình để xoay các hình 3 chiều.",
    walkthrough: [
      "Kiểm tra 'Shape A' và 'Shape B'.",
      "Kéo ngón tay qua màn hình để xoay hai hình và nhìn chúng từ mọi góc.",
      "Quay tâm trí một hình và cố gắng đẩy nó vào khoảng trống của hình khác.",
      "Nhấn \"YES\" một cách hoàn hảo, hoặc \"Không\" nếu họ không làm.",
    ],
    strategies: [
      "Đếm số khối trong cả hai hình; tổng số của chúng phải bằng tổng khối của khối rắn.",
      "Hãy tìm những vết hằn nổi bật trên một hình và tìm những vết in tương ứng ở hình kia.",
      "Xoay các hình dạng để định vị trí trục của chúng, làm cho nó dễ dàng hơn để hình dung phù hợp với chúng.",
    ],
  ),
  "kakurasu_sums": (
    objective: "Tế bào bóng trong một lưới để tổng khối lượng của các tế bào có bóng tương ứng với tổng số lượng mục tiêu cho mỗi hàng và cột.",
    controls: "Gõ vào một xà lim để thay đổi trạng thái bóng mát của nó.",
    walkthrough: [
      "Chú ý các khối nặng (1, 2, 3, 4...) nằm ở các cạnh trên và bên trái của lưới.",
      "Kiểm tra tổng số mục tiêu nằm ở các cạnh phải và dưới.",
      "Một tế bào được tô màu ở cột 3 cộng thêm 3 vào tổng của hàng.",
      "Tiếp tục làm bóng cho đến khi tất cả các hàng và cột mục tiêu chuyển sang màu xanh lá cây.",
    ],
    strategies: [
      "Tìm những con số mục tiêu cao cần thiết hầu hết các tế bào trong một hàng/column cần được tô mờ.",
      "Tìm những mục tiêu thấp (như 1 hoặc 2) nơi chỉ có thể tô bóng một tế bào.",
      "Sử dụng tham khảo chéo: bóng một tế bào ảnh hưởng đến cả hàng và cột tổng cộng cùng một lúc.",
    ],
  ),
  "kakuro": (
    objective: "Điền các chữ số từ 1 đến 9 vào ô trắng. Tổng trong từng dãy ngang và dọc phải bằng số gợi ý. Mỗi chữ số chỉ dùng một lần trong một dãy.",
    controls: "Bấm một ô trắng rồi chọn số trên bàn phím của trò chơi. Dùng nút xóa để bỏ số trong ô.",
    walkthrough: [
      "Tìm ô gợi ý có đường chéo.",
      "Số ở góc trên bên phải là tổng của dãy ngang bên phải ô gợi ý. Số ở góc dưới bên trái là tổng của dãy dọc bên dưới.",
      "Chọn ô trắng và nhập một chữ số từ 1 đến 9.",
      "Kiểm tra mỗi dãy để tránh lặp chữ số.",
    ],
    strategies: [
      "Hai ô có tổng là 3 chỉ có thể là 1 và 2. Hai ô có tổng là 4 chỉ có thể là 1 và 3.",
      "Bắt đầu ở giao điểm của hai dãy có ít cách điền.",
      "Ghi nháp các chữ số có thể điền vào từng ô.",
    ],
  ),
  "kenken": (
    objective: "Điền vào lưới với số 1 đến N ( cỡ nóng) mà không lặp lại trong bất kỳ hàng hay cột nào, như vậy các con số trong mỗi dấu 'cage' đạt được giá trị đích bằng thao tác toán học đã xác định.",
    controls: "Hãy gõ vào một tế bào để chọn nó, rồi gõ một số trên numpad. Hãy dùng biểu tượng không gian phía sau để rõ ràng.",
    walkthrough: [
      "Xem các lồng (những khu vực đáng sợ) và các manh mối mục tiêu (v. g., '3+', '12x').",
      "Tìm những cái lồng đơn tế bào, không cần toán học và cho bạn những con số miễn phí.",
      "Gõ các ô rỗng và số đầu vào thỏa mãn hoạt động toán học trong lồng.",
      "Bảo đảm không có số lặp lại trong bất kỳ hàng hoặc cột.",
    ],
    strategies: [
      "Bắt đầu với các lồng đơn tế bào và lồng với chỉ một số tổ hợp có thể (ví dụ, '3+' trong một cái lồng 2 tế bào phải là 1 và 2).",
      "Hãy nhớ rằng trừ và các lồng phân chia có thể có số trong bất kỳ thứ tự (v.g.), một chiếc lồng '2) có thể là 4 và 2, hoặc 2 và 4)",
      "Sử dụng loại bỏ theo kiểu Sudoku để xác định vị trí chính xác của con số trong một cái lồng.",
    ],
  ),
  "klotski": (
    objective: "Di chuyển khối 2x2 HO đến khu vực thoát hiểm ở giữa bảng bằng cách trượt những khối cản đường.",
    controls: "Gõ một khối để chọn nó, sau đó gõ các mũi tên hướng xuất hiện trên nó, hoặc kéo khối để di chuyển nó vào một khoảng trống.",
    walkthrough: [
      "Xác định khối 2x2 HO.",
      "Di chuyển các khối nhỏ hơn xung quanh để xóa sạch một con đường xuống.",
      "Tiếp tục trượt các khối vào khoảng trống mà không chồng chéo.",
      "Đến khu vực thoát hiểm xanh ở phía dưới cùng với khu HO để giành chiến thắng.",
    ],
    strategies: [
      "Tập trung vào việc di chuyển khối nhỏ hơn 1x1 vào những khoảng trống để giải phóng những khối lớn hơn.",
      "Cố gắng giữ khoảng trống cùng nhau để cho phép khối 2x2 lớn di chuyển.",
    ],
  ),
  "laser_link": (
    objective: "Hãy đặt những tấm gương phản chiếu tia laser từ nguồn để nó chạm tới tất cả các vị trí mục tiêu.",
    controls: "Gõ vào ô rỗng trong lưới để tuần tự các kiểu gương (sau đó cắt '/' hoặc gạch sau '\\).",
    walkthrough: [
      "Quan sát vị trí nguồn laser và hướng đầu tiên của nó.",
      "Chú ý vị trí mục tiêu laser phải đạt được.",
      "Các tế bào lưới đập để đặt gương và phản chiếu đường laser.",
      "Bảo đảm tia laser bắn trúng tất cả các mục tiêu để hoàn thành cấp độ.",
    ],
    strategies: [
      "Theo dõi đường đi bằng laser từ mục tiêu để tìm ra nơi cần có gương.",
      "Thử nghiệm với cả hai kiểu gương để tìm các góc phản chiếu chính xác.",
    ],
  ),
  "letter_bridge": (
    objective: "Tìm chữ cái đơn tạo thành một từ hợp lệ khi được thêm vào cuối chữ thứ nhất, và cũng hình thành một từ hợp lệ khi được thêm vào đầu của chữ thứ hai.",
    controls: "Gõ hay chọn đúng chữ cái để điền vào chỗ trống.",
    walkthrough: [
      "Đọc từ đầu tiên và từ thứ hai được trình bày trên màn hình.",
      "Hãy nghĩ đến một lá thư có thể kết thúc từ đầu tiên và bắt đầu từ thứ hai.",
      "Nhập chữ vào hai từ.",
      "Nếu đúng, cả hai từ mới sẽ được xác nhận và bạn thắng.",
    ],
    strategies: [
      "Kiểm tra các nguyên âm thông thường và các phụ âm thường bắt đầu hoặc kết thúc các từ.",
      "Tập trung vào từ ngắn hơn hoặc hạn chế hơn trước tiên để thu hẹp lựa chọn.",
    ],
  ),
  "letter_cancellation": (
    objective: "Tìm và chọn tất cả các trường hợp trong thư mục đích từ lưới điện tử trong khi bỏ qua sự phân tâm.",
    controls: "Gõ vào những miếng đá có chứa chữ cái đích để chọn chúng.",
    walkthrough: [
      "Xác định chữ cái đích cần tìm ngay từ đầu.",
      "Hãy quét cẩn thận lưới để tìm chữ cái đích.",
      "Gõ đúng từng chữ.",
      "Tìm mọi trường hợp để hoàn thành mạng lưới.",
    ],
    strategies: [
      "Quét hàng hoặc cột theo hàng có hệ thống để đảm bảo bạn không bỏ lỡ bất kỳ.",
      "Bỏ qua những lá thư có vẻ giống nhau được đặt làm kẻ đánh lạc hướng.",
    ],
  ),
  "letter_frequency_scan": (
    objective: "Đếm chính xác bao nhiêu lần một lá thư cụ thể xuất hiện trong đoạn văn.",
    controls: "Hãy nhập số chính xác của chữ cái đích bằng cách dùng bảng số.",
    walkthrough: [
      "Đọc lá thư bạn cần đếm.",
      "Xem lại đoạn và đếm từng trường hợp của lá thư.",
      "Bắt đầu đếm lần cuối.",
      "Kết quả chính xác để chiến thắng.",
    ],
    strategies: [
      "Đếm từng từ thay vì lướt nhanh.",
      "Hãy đọc lớn tiếng hoặc theo dõi chữ bằng ngón tay để theo dõi.",
    ],
  ),
  "letter_grid_swapper": (
    objective: "Sắp xếp lại các chữ cái trong lưới 3x3 bằng cách trao đổi các miếng cạnh nhau để tạo thành ba từ đích theo chiều ngang.",
    controls: "Gõ một miếng gạch để chọn, rồi gõ một miếng gạch kế bên để đổi vị trí.",
    walkthrough: [
      "Hãy nhìn vào ba từ TARGET được hiển thị ở đầu trang.",
      "Tìm các chữ cái cho từ đầu tiên và chuyển chúng lên hàng đầu.",
      "Gõ một miếng gạch, rồi gõ một miếng gạch kế bên để trao đổi.",
      "Hoàn tất cả ba từ theo chiều ngang để ghi điểm và tạo ra một câu đố mới.",
    ],
    strategies: [
      "Tập trung vào việc tạo ra từng từ một, bắt đầu từ hàng đầu.",
      "Hãy cẩn thận đừng lẫn lộn các chữ cái của từ đã được viết xong.",
    ],
  ),
  "lighthouses": (
    objective: "Đặt thuyền trong lưới để mỗi ngọn hải đăng chỉ đúng số tàu trong hàng và cột.",
    controls: "Các tế bào mạng lưới đập vào vị trí hoặc loại bỏ tàu.",
    walkthrough: [
      "Hãy nhìn những con số trên mỗi ngọn hải đăng.",
      "Đặt thuyền cùng hàng hoặc cột với ngọn hải đăng để khớp với con số của nó.",
      "Những chiếc tàu bảo đảm không chạm vào nhau hay những ngọn hải đăng, ngay cả hai bên nhau.",
      "Thỏa mãn mọi điều kiện hải đăng để chiến thắng.",
    ],
    strategies: [
      "Bắt đầu với những ngọn hải đăng có số 0 và đánh dấu hàng và cột trống.",
      "Tìm những con đường chồng chéo giữa những ngọn hải đăng với số lượng cao.",
    ],
  ),
  "lights_out": (
    objective: "Tắt tất cả đèn trên lưới đi, bật đèn lên tình trạng và trạng thái ánh sáng kề bên.",
    controls: "Đập một miếng gạch để bật lên cùng với hàng xóm gần nhất (lên, xuống, trái, phải).",
    walkthrough: [
      "Quan sát mẫu ban đầu của những miếng gạch sáng và chưa sáng.",
      "Gõ một miếng gạch để tắt nó, để ý cách nó lật đổ những người hàng xóm.",
      "Hãy băng qua lưới điện để tắt đèn một cách có hệ thống.",
      "Achieve một bảng tối để giành chiến thắng.",
    ],
    strategies: [
      "Cố gắng giải quyết từng hàng, tắt mọi đèn trong hàng hiện thời bằng cách nhấn vào hàng bên dưới.",
      "Dùng mẫu để giải quyết hàng cuối nếu bạn bị kẹt.",
    ],
  ),
  "lock_pattern": (
    objective: "Ghi nhớ và tái tạo mẫu khoá hiển thị bằng cách kết nối các chấm theo thứ tự chính xác.",
    controls: "Kéo ngón tay qua các chấm để vẽ mô hình.",
    walkthrough: [
      "Xem mẫu được vẽ trên lưới.",
      "Ghi nhớ trình tự và hướng chính xác.",
      "Vượt qua các dấu chấm để tái tạo lại chuỗi.",
      "Hãy thả ngón tay ra khi mẫu hình được hoàn tất.",
    ],
    strategies: [
      "Phá vỡ các mẫu phức tạp thành các hình dạng hình học đơn giản.",
      "Hãy hình dung một con đường hoặc chỉ định những con số để nhớ các dấu chấm.",
    ],
  ),
  "logical_syllogisms": (
    objective: "Xác định nếu một kết luận hợp lý theo sau từ các cơ sở cho.",
    controls: "Gõ 'Valid' hay 'Ivald' dựa trên suy luận của anh.",
    walkthrough: [
      "Hãy đọc kỹ những lời được cung cấp.",
      "Hãy đọc lời kết luận của những lời này.",
      "Quyết định nếu kết luận là một sự kiện chắc chắn chỉ dựa trên lời tuyên bố.",
      "Gõ đúng lựa chọn xác thực.",
    ],
    strategies: [
      "Bỏ qua thực tế thế giới thực; câu trả lời của bạn chỉ dựa trên logic trình bày.",
      "Vẽ biểu đồ Venn tâm trí để vẽ bản đồ 'All', 'Một số', hoặc 'No'.",
    ],
  ),
  "magic_squares": (
    objective: "Điền vào lưới với số lượng để mỗi hàng, cột, và đường chéo thêm vào cùng một tổng mục tiêu.",
    controls: "Gõ vào một phòng trống và chọn một số để đặt nó.",
    walkthrough: [
      "Kiểm tra tổng mục tiêu.",
      "Tìm một hàng, cột, hoặc chéo với chỉ một số bị thiếu.",
      "Tính giá trị bị mất và đặt nó.",
      "Nhắc lại, cho đến khi toàn bộ hệ thống được lấp đầy.",
    ],
    strategies: [
      "Luôn luôn giải quyết các dòng với những con số lớn nhất điền vào đầu tiên.",
      "Tế bào trung tâm rất quan trọng; việc tìm ra nó sớm sẽ giúp phần còn lại dễ dàng hơn.",
    ],
  ),
  "magnets": (
    objective: "Nơi nam châm hìnhmino (với + và - cực) vì vậy chúng thỏa mãn các hạn chế số đếm hàng/column và các cực giống hệt nhau không chạm vào.",
    controls: "Tế bào đập để bật/tắt giữa +, -, và trống.",
    walkthrough: [
      "Kiểm tra các con số ở cạnh lưới cho thấy có bao nhiêu + và - cực trong mỗi hàng/column.",
      "Hãy nhớ rằng + không thể chạm đến + và - không thể chạm - bất cứ nơi nào.",
      "Điền vào nửa từ.",
      "Đánh dấu các dây dẫn không từ tính trống để hoàn thành lưới.",
    ],
    strategies: [
      "Hàng hoặc cột với một số 0 có thể ngay lập tức được lấp đầy với trống.",
      "Nếu một đô-mi-nô phải có từ tính, đặt một cực đẩy các cực khác.",
    ],
  ),
  "mandala_recall": (
    objective: "Ghi nhớ màu sắc của mô hình mandala và tái tạo lại nó từ trí nhớ.",
    controls: "Đánh một màu từ bảng màu, rồi gõ vào các phần mandala để sơn chúng.",
    walkthrough: [
      "Hãy nghiên cứu kỹ lưỡng ma - na - la màu sắc trong giai đoạn ký ức.",
      "Một khi các màu đã biến mất, hãy chọn màu từ bảng chọn bên dưới.",
      "Gõ đúng phần mandala để áp dụng màu sắc.",
      "Điền đầy đủ các phần màu sắc để giành chiến thắng.",
    ],
    strategies: [
      "Tập trung vào đối xứng; nếu bên trái là màu đỏ, bên phải có thể là quá.",
      "Ghi nhớ từng lớp, bắt đầu từ trung tâm bên ngoài.",
    ],
  ),
  "math_guess": (
    objective: "Đoán rằng phương trình toán học ẩn trong số lần thử, sử dụng các gợi ý màu cho các số chính xác và các nhà điều hành.",
    controls: "Dùng bàn phím trên màn hình để gõ một phương trình và nạp tap.",
    walkthrough: [
      "Hãy nhập một phương trình hợp lệ bằng số đích.",
      "Xem phản hồi màu (ví dụ, xanh lá cây cho điểm đúng, vàng cho điểm sai).",
      "Điều chỉnh phương trình bằng phản hồi.",
      "Tìm phương trình ẩn chính xác trước khi bạn hết thử.",
    ],
    strategies: [
      "Bắt đầu với một phương trình sử dụng các con số và hoạt động đa dạng.",
      "Hãy nhớ thứ tự các ca phẫu thuật (PEMDAS) áp dụng cho các phỏng đoán của bạn.",
    ],
  ),
  "math_maze": (
    objective: "Di chuyển qua mê cung bằng cách di chuyển đến các tế bào lân cận thỏa mãn các điều kiện toán học hoặc giá trị mục tiêu.",
    controls: "Đánh hay chạm vào các tế bào kế bên để chuyển nhân vật của bạn qua mê cung.",
    walkthrough: [
      "Hãy lưu ý giá trị bắt đầu và quy tắc toán học cho mê cung.",
      "Tính toán kết quả của việc di chuyển đến các tế bào lân cận.",
      "Chọn con đường giữ giá trị đúng hoặc khớp chuỗi.",
      "Đến được chỗ gạch thoát hiểm để hoàn thành mê cung.",
    ],
    strategies: [
      "Nhìn trước vài bước để tránh những ngõ cụt phá vỡ quy tắc toán học.",
      "Làm việc từ lối ra sau nếu con đường phía trước gây nhầm lẫn.",
    ],
  ),
  "math_path": (
    objective: "Tìm một con đường của số và các nhà điều hành mà đánh giá đến kết quả mục tiêu.",
    controls: "Trượt qua các miếng cạnh nhau để tạo thành một biểu thức toán học hợp lệ.",
    walkthrough: [
      "Hãy nhìn vào số mục tiêu bạn cần để liên lạc.",
      "Tìm số khởi động trên mạng đi.",
      "Vượt qua các nhà điều hành và các con số để xây dựng một phương trình.",
      "Thả ngón tay ra khi phương trình bằng đích.",
    ],
    strategies: [
      "Nếu mục tiêu là lớn, tìm kiếm các miếng nhân.",
      "Theo dõi toàn bộ sự chạy trong đầu bạn khi bạn vẽ đường đi.",
    ],
  ),
  "matrix_multiplier": (
    objective: "Thực hiện phép nhân ma trận để tính toán kết quả đúng ma trận kết quả.",
    controls: "Hãy gõ các tế bào kết quả và nhập vào các con số tính toán.",
    walkthrough: [
      "nhìn vào hai ma trận được nhân.",
      "Nhân hàng của ma trận thứ nhất với cột thứ hai.",
      "Gõ một tế bào vào ma trận kết quả.",
      "Hãy nhập tổng các sản phẩm để điền vào ma trận.",
    ],
    strategies: [
      "Viết xuống các bước trung gian về mặt tinh thần hoặc sử dụng khăn giấy nếu cần thiết.",
      "Kiểm tra 2 lần tích cực và âm tính cẩn thận.",
    ],
  ),
  "matrix_multiplier_match": (
    objective: "Khớp cặp ma trận với chính xác nhân kết quả.",
    controls: "Gõ một biểu thức ma trận và sau đó gõ kết quả tương ứng của nó để phù hợp với chúng.",
    walkthrough: [
      "Xem danh sách các cặp ma trận và danh sách kết quả.",
      "Tính toán nhanh hoặc tính toán phép nhân của một cặp.",
      "đập đôi và vỗ vào kết quả khớp.",
      "Xoá mọi mục trong màn hình để giành chiến thắng.",
    ],
    strategies: [
      "Tính toán chỉ các yếu tố trên bên trái kết quả để nhanh chóng tìm thấy phù hợp.",
      "Tìm ma trận với số không để tăng tốc tính toán.",
    ],
  ),
  "matrix_reasoning": (
    objective: "Xác định mẫu còn thiếu trong ma trận thị giác từ các lựa chọn cho trước.",
    controls: "Gõ chính xác mô hình thị giác từ các tùy chọn bên dưới ma trận.",
    walkthrough: [
      "Quan sát lưới 3x3 mẫu với một mảnh còn thiếu.",
      "Tìm quy tắc hợp lý quản lý hàng và cột (ví dụ, luân phiên, thêm).",
      "Áp dụng quy tắc để xác định phần còn thiếu nên trông như thế nào.",
      "Gõ tùy chọn tương ứng để giải quyết.",
    ],
    strategies: [
      "Kiểm tra một tính năng tại một thời điểm: màu đầu tiên, rồi hình dạng, rồi quay.",
      "Kiểm tra lý thuyết của bạn trên cả một hàng và một cột để chắc chắn.",
    ],
  ),
  "maze_nav_3d": (
    objective: "Di chuyển qua một mê cung 3D để tìm lối thoát từ góc nhìn người đầu tiên.",
    controls: "Dùng nút điều hướng trên màn hình hoặc kéo về phía trước, đằng sau và xoay.",
    walkthrough: [
      "Hãy nhìn xung quanh để định hướng bạn trong môi trường 3D.",
      "Di chuyển về phía trước qua hành lang.",
      "Ghi nhớ các giao lộ để tránh đi thành vòng tròn.",
      "Tìm cánh cửa thoát hiểm hoặc cánh cổng để thắng.",
    ],
    strategies: [
      "Dùng 'luật tay phải': luôn luôn giữ tay phải trên tường để cuối cùng tìm thấy lối thoát.",
      "Hãy tìm ra những kết cấu hay những điểm mốc đặc biệt để nhớ về nơi bạn đã ở.",
    ],
  ),
  "memory_matrix": (
    objective: "Ghi nhớ những miếng gạch đã tô sáng và vỗ vào chúng sau khi chúng được giấu đi.",
    controls: "Đập những viên gạch mà anh còn nhớ đã được đánh dấu.",
    walkthrough: [
      "quan sát lưới điện khi những mảnh gạch nào đó sáng lên.",
      "Ghi nhớ vị trí chính xác của chúng.",
      "Chờ cho những viên gạch lật lại.",
      "Gõ tất cả các mảnh sáng trước đây đúng.",
    ],
    strategies: [
      "Tìm kiếm các hình hoặc chữ cái được tạo ra bởi các miếng được tô sáng.",
      "Đừng vội vã, một khi bạn đã chắc chắn về mô hình, vòi nước có hệ thống.",
    ],
  ),
  "memory_palace": (
    objective: "Liên kết các vật dụng với những địa điểm cụ thể trong một căn phòng và nhớ lại sau đó.",
    controls: "Hãy gõ các địa điểm trong phòng và chọn đúng mục trong danh sách.",
    walkthrough: [
      "Quan sát những vật dụng đặt tại nhiều địa điểm khác nhau trong phòng.",
      "Tạo một câu chuyện tinh thần liên kết mục này với địa điểm.",
      "Một khi mục đã được giấu, hãy gõ một địa điểm.",
      "Chọn mục thuộc về nơi này từ các tùy chọn.",
    ],
    strategies: [
      "Làm cho các mối liên hệ tâm thần của bạn kỳ lạ hoặc vui nhộn - họ dễ dàng hơn để nhớ.",
      "Hãy hình dung việc đi bộ trong phòng theo một con đường cụ thể.",
    ],
  ),
  "mental_abacus": (
    objective: "Thực hiện các tính toán bằng cách hình ảnh hóa abacus và di chuyển hạt của nó trong tâm trí.",
    controls: "Hãy nhập số cuối cùng được tính bằng bàn phím.",
    walkthrough: [
      "Đọc chuỗi số để thêm hay trừ.",
      "Tâm trí di chuyển chuỗi hạt trên một bàn đạp tưởng tượng.",
      "Theo dõi vị trí vòng cuối cùng.",
      "Gõ vào kết quả số cuối cùng.",
    ],
    strategies: [
      "Hãy quen thuộc với giá trị của hạt ở trên ( 5) và dưới (1) hạt.",
      "Dùng ngón tay để bắt chước việc di chuyển hạt trong không khí.",
    ],
  ),
  "mental_calendar": (
    objective: "Tính ngày của tuần cho một cuộc hẹn ngẫu nhiên.",
    controls: "Đánh đúng ngày trong tuần từ nhiều lựa chọn.",
    walkthrough: [
      "Xem ngày trên màn hình.",
      "Áp dụng luật ngày tận thế hoặc thuật toán lịch toán tương tự.",
      "Tính toán ngày neo và bù đắp.",
      "Chọn ngày kết thúc trong tuần.",
    ],
    strategies: [
      "Ghi nhớ mã tháng và thế kỷ trước.",
      "Thực hành tìm ngày neo trong năm nay để tăng tốc độ tính toán.",
    ],
  ),
  "mental_mapping": (
    objective: "Theo một loạt hướng dẫn trong trí và xác định vị trí cuối cùng trên bản đồ.",
    controls: "Mở di động điểm đến cuối cùng trên mạng lưới.",
    walkthrough: [
      "Hãy chú ý vị trí khởi hành của bạn trên mạng lưới.",
      "Đọc hoặc nghe chuỗi chuyển động theo hướng (v.G., North, East).",
      "Theo dõi các chuyển động tâm trí mà không chạm vào màn hình.",
      "Gõ vào xà lim cuối cùng nơi con đường kết thúc.",
    ],
    strategies: [
      "Hủy bỏ những nước đi đối diện trong đầu (ví dụ g., lên sau đó xuống có nghĩa là bạn không di chuyển).",
      "Hãy chăm chú nhìn điểm bắt đầu và tập trung vào đúng như lời chỉ dẫn.",
    ],
  ),
  "mental_rotation": (
    objective: "Xác định nếu hai hình ba chiều giống hệt nhau, nhưng xoay, hoặc quay ảnh.",
    controls: "Gõ 'Match' hay 'Different' dựa trên sự hình dung không gian của bạn.",
    walkthrough: [
      "Xem cấu trúc khối ba chiều chính.",
      "Hãy nhìn vào cấu trúc khối 3D thứ hai.",
      "Thay đổi tâm trí cấu trúc đầu tiên để thẳng hàng với cái thứ hai.",
      "Quyết định xem chúng có cùng hình dạng hay là phiên bản phản chiếu.",
    ],
    strategies: [
      "Tập trung vào một tính năng đặc biệt hoặc 'arm' của hình dạng và theo dõi của nó quay.",
      "Cố gắng nhận diện sự thuận tay (bên trái/phải) của các phần đối xứng.",
    ],
  ),
  "minesweeper": (
    objective: "Dọn sạch cái bảng mà không làm nổ bất kỳ quả mìn bị ẩn nào, sử dụng những manh mối đánh số cho thấy những quả mìn bên cạnh.",
    controls: "Đánh một tấm gạch để lộ nó.",
    walkthrough: [
      "Gõ một ô vuông ngẫu nhiên để mở một khu vực khởi đầu.",
      "nhìn vào các con số; một '1' có nghĩa là chính xác một mỏ là gần nó.",
      "Nhấn mạnh để đặt một lá cờ nơi bạn chắc chắn một mỏ tồn tại.",
      "cách an toàn, hãy đập tất cả những viên gạch không phải của tôi để hoàn thành cấp độ.",
    ],
    strategies: [
      "Nếu một chữ '1' chỉ chạm vào một viên gạch chưa được đánh dấu, viên gạch đó phải là một mỏ.",
      "Một khi bạn đánh dấu đúng số mìn xung quanh một con số, tất cả các mảnh kế bên sẽ an toàn.",
    ],
  ),
  "mirror_image": (
    objective: "Xác định hình phản chiếu chính xác của hình hoặc hình ảnh được trình bày.",
    controls: "Ghi lại hình ảnh phản chiếu chính xác từ danh sách các tùy chọn đa chọn.",
    walkthrough: [
      "Cẩn thận quan sát hình ảnh đích được trình bày lúc đầu.",
      "Kiểm tra các lựa chọn đa lựa chọn được trình bày.",
      "phản ánh tâm trí ảnh đích dọc theo trục được chỉ định.",
      "Gõ lại tùy chọn phù hợp với suy nghĩ của bạn để tiến bộ.",
    ],
    strategies: [
      "Tập trung vào những chi tiết không đối xứng như các nếp nhăn hoặc màu sắc.",
      "Chọn một điểm cụ thể trên mục tiêu và tìm ra nơi nó nên kết thúc sau khi lật.",
      "Loại bỏ rõ ràng các lựa chọn sai trước tiên để cải thiện tỷ lệ cược của bạn.",
    ],
  ),
  "mirror_maze": (
    objective: "Chuyển tia laser hoặc ánh sáng xuyên qua mê cung đến mục tiêu bằng cách đặt gương.",
    controls: "Các tế bào lưới đập vào vị trí hoặc quay gương để làm lệch đường đi.",
    walkthrough: [
      "Xác định điểm bắt đầu của tia và mục tiêu cuối cùng.",
      "Lưu ý các chướng ngại vật và khoảng trống trong lưới.",
      "Tap để đặt một tấm gương và vỗ một lần nữa để xoay nó.",
      "Sắp xếp các gương để tia phản xạ phản xạ ở góc 90 độ để đạt được mục tiêu.",
    ],
    strategies: [
      "Làm việc ngược từ mục tiêu để tìm ra sự phản ánh cần thiết cuối cùng.",
      "Hãy đếm số lượng những tấm gương có sẵn; bạn có thể cần dùng tất cả chúng.",
      "Tránh đặt những tấm gương nơi tia sáng sẽ chạm phải chướng ngại vật.",
    ],
  ),
  "mirror_tracing": (
    objective: "Theo dõi một hình dạng nhất định càng chính xác càng tốt trong khi đầu vào của bạn được phản ánh.",
    controls: "Kéo ngón tay qua màn hình để vẽ; các nét vẽ của bạn sẽ xuất hiện phản ánh.",
    walkthrough: [
      "Hãy nhìn vào các đường nét chấm của hình dạng cần theo dõi.",
      "Đặt ngón tay lên điểm xuất phát.",
      "Kéo ngón tay để theo dõi hình dạng, điều chỉnh cho chuyển động ngược.",
      "Hoàn thành đầy đủ các nét vẽ với sự lệch hướng tối thiểu để đạt được điểm cao.",
    ],
    strategies: [
      "Di chuyển chậm rãi và cố ý, đặc biệt là xung quanh các góc.",
      "Tập trung nhìn vào đầu đề chứ không phải ngón tay.",
      "Đoán trước hướng ngược lại trước khi hành động.",
    ],
  ),
  "missing_operator": (
    objective: "Điền vào những nhà toán học bị mất tích để làm cho các phương trình cho trước đúng.",
    controls: "Gõ vào một rãnh điều khiển trống, rồi gõ vào người điều hành ưa thích (+, -, ×,  vội.)",
    walkthrough: [
      "Phân tích các số cho trước và kết quả đích của phương trình.",
      "Hãy ước lượng xem chiến dịch nào sẽ đưa bạn đến gần mục tiêu hơn.",
      "Gõ trống khe trống và chèn người điều hành.",
      "Trò chơi kiểm tra nếu phương trình đã điền đánh giá tới kết quả đích.",
    ],
    strategies: [
      "Hãy nhớ thứ tự của các thao tác (unintelligible/division trước khi thêm vào tập tin).",
      "Nếu mục tiêu lớn hơn nhiều so với các nhà hát opera, rất có thể bạn cần phép nhân.",
      "Nếu mục tiêu nhỏ hay nhỏ, hãy tìm sự phân chia hoặc phép trừ.",
    ],
  ),
  "missing_vowels": (
    objective: "Xác định từ đúng bằng cách điền vào các nguyên âm bị thiếu.",
    controls: "Gõ các nguyên âm chính xác từ bàn phím để hoàn thành từ.",
    walkthrough: [
      "Đọc khung xương phụ của từ và manh mối kèm theo.",
      "Cố gắng phát âm những từ phù hợp với phụ âm.",
      "Gõ các phím nguyên âm theo đúng trình tự.",
      "Hoàn tất từ để chuyển sang thử thách tiếp theo.",
    ],
    strategies: [
      "Hãy dùng những gợi ý về bối cảnh; chúng thường làm mất đi ý nghĩa.",
      "Tìm kiếm các tiền tố và hậu tố chung có thể gợi lên các nguyên âm.",
      "Nếu bị mắc kẹt, hãy thử cắm điện vào 'E' hoặc 'A' trước, vì chúng là phổ biến nhất.",
    ],
  ),
  "modulo_clock": (
    objective: "Giải quyết các vấn đề số học sử dụng mô- đun (đồng hồ).",
    controls: "Hãy gõ các nút số để nhập vào câu trả lời đã tính toán của bạn.",
    walkthrough: [
      "Đọc mô-đun cơ bản (v.G., Modulo 12, như một đồng hồ chuẩn).",
      "Hãy nhìn vào biểu thức số học cho trước.",
      "Thực hiện tính toán và tìm phần còn lại khi chia cho cơ sở.",
      "Hãy gõ đúng câu trả lời.",
    ],
    strategies: [
      "Đối với Modulo 12, chỉ cần nghĩ về thêm hoặc trừ giờ trên một khuôn mặt đồng hồ.",
      "Nếu một con số lớn hơn mô-đun, trừ theo mô-đun cho đến khi nó nhỏ hơn.",
      "Số âm nghĩa là đếm ngược từ cơ sở mô-đun.",
    ],
  ),
  "modulo_path": (
    objective: "Tìm một đường dẫn liên tục qua một lưới nơi các con số bên cạnh thỏa mãn một quy luật mô-đun cụ thể.",
    controls: "Gõ hoặc kéo qua các tế bào lưới để tạo thành một đường dẫn hợp lệ.",
    walkthrough: [
      "Chú ý quy tắc mô- đun đích cần thiết cho đường dẫn.",
      "Bắt đầu từ ô bắt đầu được tô sáng.",
      "Chọn một tế bào kế bên để thực hiện điều kiện mô- đun so với tế bào hiện tại.",
      "Tiếp tục cho đến khi bạn đến đích.",
    ],
    strategies: [
      "Hãy nhìn trước một hoặc hai bước trước khi hành động.",
      "Nhanh chóng tính toán phần còn lại của tất cả các tế bào xung quanh để tìm ứng cử viên.",
      "Nếu anh đi vào ngõ cụt, quay lại và thử đường khác.",
    ],
  ),
  "multiple_object_tracking": (
    objective: "Theo dõi các đối tượng mục tiêu cụ thể khi chúng di chuyển ngẫu nhiên giữa các thiết bị đánh lạc hướng giống hệt nhau.",
    controls: "Đánh đập những đối tượng bạn tin tưởng là những mục tiêu gốc sau khi chúng ngừng di chuyển.",
    walkthrough: [
      "Ghi nhớ những mục được tô sáng một cách ngắn gọn lúc đầu.",
      "Tập trung vào những mục tiêu đó khi mọi mục tiêu bắt đầu di chuyển.",
      "Giữ tập trung cho đến khi mọi chuyển động dừng lại.",
      "Gõ vào chính xác những thứ đã được tô sáng ban đầu.",
    ],
    strategies: [
      "Đừng nhìn trực tiếp vào một đối tượng; hãy sử dụng một cái nhìn nhẹ nhàng, trung tâm để theo dõi toàn bộ nhóm.",
      "Tập hợp các mục tiêu trong tâm trí vào một đa giác và xem hình dạng hình dạng.",
      "Tránh để đồ vật đi ngang qua đường.",
    ],
  ),
  "multi_track_counter": (
    objective: "Giữ số lượng đồng thời của các loại vật thể xuất hiện trên màn hình.",
    controls: "Hãy gõ vào mỗi nút +/usus, hoặc nhập số lần cuối cho mỗi phân loại.",
    walkthrough: [
      "Quan sát các loại vật thể bạn cần theo dõi.",
      "Khi các vật thể xuất hiện và biến mất, hãy chuẩn bị tinh thần cho mỗi vật.",
      "Khi chuỗi thứ tự kết thúc, hãy nhập số lần cuối vào từng hạng mục.",
      "Gửi câu trả lời của bạn để xem bạn có theo dõi đúng không.",
    ],
    strategies: [
      "Lặp lại nhịp tính trong đầu (v. g., 'hai đỏ, ba xanh dương'.",
      "Sử dụng ngón tay của bạn để theo dõi một loại trong khi tâm trí theo dõi khác.",
      "Bình tĩnh và đừng hoảng sợ nếu có nhiều đồ vật xuất hiện cùng một lúc.",
    ],
  ),
  "narrative_recall": (
    objective: "Hãy đọc một câu chuyện ngắn và trả lời chính xác các câu hỏi về các chi tiết cụ thể.",
    controls: "Hãy gõ chính xác câu trả lời từ nhiều lựa chọn.",
    walkthrough: [
      "Đọc kỹ lời tường thuật được cung cấp trong thời gian hạn định.",
      "Cố gắng nhớ các chi tiết then chốt như tên, số, màu sắc và chuỗi sự kiện.",
      "Một khi câu Kinh Thánh biến mất, hãy đọc những câu hỏi thấu hiểu.",
      "Chọn câu trả lời đúng dựa trên những gì bạn nhớ.",
    ],
    strategies: [
      "Hãy hình dung câu chuyện trong trí bạn để các chi tiết dễ nhớ hơn.",
      "Hãy đặc biệt chú ý đến danh từ, ngày tháng và con số thích hợp.",
      "Đừng chỉ mơ hồ, cố gắng hiểu cốt truyện và bối cảnh thực sự.",
    ],
  ),
  "n_back": (
    objective: "Chỉ ra mục hiện thời trùng với bước trước đó.",
    controls: "Gõ 'Match' hay 'Không khớp' khi mỗi mục xuất hiện.",
    walkthrough: [
      "Ghi chú mức 'N' cho trò chơi hiện thời (ví dụ, 2- hậu phương có nghĩa là khớp với mục 2 bước trước).",
      "Quan sát chuỗi các mục (các chữ cái, hoặc vị trí) xuất hiện từng mục một.",
      "Khi mục hiện thời xuất hiện, hãy so sánh nó với bước 'N'.",
      "Nhấn nút tương ứng để đăng ký câu trả lời trước khi mục kế tiếp xuất hiện.",
    ],
    strategies: [
      "Cập nhật liên tục bộ nhớ bằng cách thả món đồ cũ nhất và thêm món mới nhất.",
      "Nói to lên chuỗi các mục 'N' cuối cùng trong đầu bạn.",
      "Tập trung vào; một sự mất tập trung có thể làm hỏng chuỗi của bạn.",
    ],
  ),
  "negative_space_detection": (
    objective: "Xác định hình hoặc chữ cái ẩn được tạo bởi khoảng trống giữa các đối tượng.",
    controls: "Gõ chính xác câu trả lời từ các tùy chọn, hoặc gõ hình được xác định.",
    walkthrough: [
      "Xem ảnh phức tạp được trình bày trên màn hình.",
      "Chuyển trọng tâm từ đối tượng rắn sang khoảng trống nền.",
      "Xác định dạng liên kết được tạo bởi khoảng trống đó.",
      "Chọn hoặc nhập câu trả lời đúng.",
    ],
    strategies: [
      "Cố gắng nhắm mắt hoặc thư giãn mắt để che đi cảnh quan.",
      "Hãy nhìn vào các cạnh của các vật thể rắn; chúng tạo thành các đường nét của hình thù tiêu cực.",
      "Đổi màu sắc trong trí (hình dung nền là màu đen và đồ vật màu trắng).",
    ],
  ),
  "nonogram": (
    objective: "Điền vào một mạng lưới dựa trên manh mối số để tiết lộ một hình ảnh nghệ thuật điểm ảnh ẩn.",
    controls: "Gõ vào một tế bào để điền vào, gõ một lần nữa để đánh dấu nó là trống (X), hoặc nhấn dài để kéo.",
    walkthrough: [
      "Xem những con số ở đầu mỗi hàng và cột, cho thấy các tế bào được lấp đầy liên tục.",
      "Dùng manh mối cắt nhau để suy luận tế bào nào cần được lấp đầy.",
      "Các ô đánh dấu phải trống với dấu X để thu hẹp các khả năng.",
      "Tiếp tục giảm dần cho đến khi toàn bộ lưới được lấp đầy.",
    ],
    strategies: [
      "Bắt đầu với những con số lớn nhất, đặc biệt là những con số chiếm hơn một nửa hàng /column.",
      "Luôn đánh dấu những khoảng trống với một chữ X một khi bạn hoàn thành một khối manh mối.",
      "Không bao giờ đoán; mỗi bước nên dựa trên logic thuần túy.",
    ],
  ),
  "norinori": (
    objective: "Đánh bóng chính xác hai tế bào trong mỗi vùng được xác định, đảm bảo không có tế bào bóng chạm chéo hoặc chia nhỏ các biên giới thành nhiều nhóm lớn hơn hai.",
    controls: "Các tế bào đập để bật lên trạng thái bóng râm của chúng, hoặc đánh dấu chúng là hoàn toàn trống rỗng.",
    walkthrough: [
      "Hãy nhìn vào mạng lưới chia thành những vùng được vạch rõ một cách dạn dĩ.",
      "Đánh bóng đúng hai tế bào trên mỗi khu vực.",
      "Hãy chắc chắn rằng mỗi tế bào có bóng sẽ chia sẻ chính xác một cạnh với một tế bào khác có bóng mát (hình đô - mi - min).",
      "Hãy chắc chắn rằng không dây đô - mi - nô nào đụng đến một dây chuyền khác, thậm chí không chéo.",
    ],
    strategies: [
      "Nếu một vùng chỉ có hai tế bào, cả hai phải được tô màu.",
      "Một khi bạn đặt một đô-mi-nô, bao quanh nó với những dấu vết trống bởi vì không ai khác có thể chạm vào nó.",
      "Dùng lý luận góc để suy luận nơi mà dây domino buộc phải đi.",
    ],
  ),
  "number_bonds": (
    objective: "Hoàn tất số trái phiếu bằng cách tìm phần còn thiếu hợp với toàn bộ số đã cho.",
    controls: "Gõ nút còn thiếu và dùng bảng số để nhập giá trị đúng.",
    walkthrough: [
      "nhìn vào số trung tâm và số 'part' kết nối.",
      "Trừ những phần đã biết ra để tìm ra giá trị còn thiếu.",
      "Nhập số chính xác vào vòng tròn rỗng.",
      "Hoàn tất mọi liên kết trên màn hình để tiến hành.",
    ],
    strategies: [
      "Sử dụng phép trừ để tìm một phần còn thiếu, và thêm vào để tìm một phần còn thiếu.",
      "Ghi nhớ sự kết hợp của 10 và 100 để tăng tốc tính toán.",
      "Kiểm tra lại hai lần trước khi gửi câu trả lời cuối cùng.",
    ],
  ),
  "numerical_estimation": (
    objective: "Ước tính số mục hoặc kết quả của một tính toán phức tạp mà không đếm chính xác.",
    controls: "Hãy chọn ước lượng gần nhất trong danh sách, hoặc điều chỉnh con trượt theo giá trị đoán.",
    walkthrough: [
      "Một nhóm lớn các mục hoặc một vấn đề toán học phức tạp xuất hiện ngắn gọn.",
      "Hãy ước lượng nhanh số lượng hoặc câu trả lời.",
      "Chọn tùy chọn gần nhất với ước lượng của bạn.",
      "Ghi điểm dựa trên ước tính của bạn về con số thật.",
    ],
    strategies: [
      "Đừng cố đếm từng món đồ một, bạn sẽ không có thời gian.",
      "Đếm một phần phụ nhỏ (như một phần tư) và nhân với tổng số phần.",
      "Đối với các vấn đề toán học, vòng con số đến gần nhất mười hoặc trăm trước khi tính toán.",
    ],
  ),
  "nurikabe": (
    objective: "Tạo ra \"là vùng đất\" của các tế bào trắng chứa chính xác một số, được bao quanh bởi một \"con sông\" liên tục của các tế bào đen.",
    controls: "Tế bào đập để đánh dấu chúng là đen (bên dòng chảy) hay màu trắng (tức là đất liền).",
    walkthrough: [
      "Hãy nhìn vào lưới chứa các con số, mỗi con số là một phần của một hòn đảo có kích cỡ chính xác như thế.",
      "Kiểm tra tất cả các ô màu đen tạo thành một mạng kết nối duy nhất.",
      "Chắc chắn không có 2x2 ô màu đen ở bất cứ đâu.",
      "Hoàn tất lưới bằng cách xác định chính xác tất cả các đảo và dòng sông.",
    ],
    strategies: [
      "Một tế bào chứa một chiếc '1' là hòn đảo riêng của nó, nên bao quanh nó hoàn toàn bằng các tế bào đen.",
      "Khi hai hòn đảo đến quá gần nhau, hãy tách chúng ra với một bức tường các tế bào đen.",
      "Nếu một khối tế bào đen sắp hình thành một hình vuông 2x2, hãy để lại một ô trắng.",
    ],
  ),
  "object_displacement": (
    objective: "Xác định đối tượng nào đã được di chuyển hay trao đổi sau khi màn hình tắt trống.",
    controls: "Đập vào vật thể đã thay đổi vị trí.",
    walkthrough: [
      "Ghi nhớ bố trí và vị trí của mọi đối tượng trên màn hình.",
      "Chờ cho màn hình chớp mắt hoặc để các vật thể được giấu một thời gian ngắn.",
      "Quan sát bố trí mới và nhận ra sự mâu thuẫn.",
      "Gõ vào vật thể ở nơi khác hơn trước.",
    ],
    strategies: [
      "Nhóm các đối tượng theo vị trí tương đối (v. g., 'apple cạnh chuối').",
      "Tập trung vào các cạnh hoặc góc của bố trí trước.",
      "Đừng cố nhớ tọa độ tuyệt đối; nhớ các mối quan hệ không gian.",
    ],
  ),
  "object_shuffle": (
    objective: "Theo dõi một đối tượng bị ẩn vì nó được xáo trộn nhanh chóng giữa các hộp giống hệt nhau.",
    controls: "Gõ vào container giữ mục tiêu sau khi dừng lại.",
    walkthrough: [
      "Cẩn thận khi đối tượng được đặt dưới một trong các thùng chứa.",
      "Hãy chú ý đến cái thùng đó khi tất cả chúng đều đổi chỗ.",
      "Chờ cho hình động giật kết thúc.",
      "Nhấn nút mà anh tin là giữ mục tiêu.",
    ],
    strategies: [
      "Đừng rời mắt khỏi vật chứa mục tiêu, dù chỉ một giây.",
      "Không cố gắng theo dõi tất cả các thùng chứa, chỉ một trong những có mục tiêu.",
      "Nếu bạn mất dấu, hãy đoán dựa trên quỹ đạo cuối cùng của nó.",
    ],
  ),
  "odd_even_flash": (
    objective: "Nhanh chóng phân loại một số nhanh chóng đăng nhanh như lẻ hoặc thậm chí.",
    controls: "Gõ vào nút 'Odd' hoặc 'Ngay cả' tương ứng với số điện thoại.",
    walkthrough: [
      "Tập trung vào trung tâm màn hình.",
      "Một số sẽ xuất hiện trong một phần của giây.",
      "Hãy xác định nếu con số này là số lẻ hoặc ngay cả.",
      "Nhấn nút đúng càng nhanh càng tốt để tối đa điểm của bạn.",
    ],
    strategies: [
      "Chỉ nhìn vào số cuối cùng của con số để xác định nó là lẻ hay thậm chí.",
      "Giữ ngón tay của bạn lơ lửng trên cả hai nút để giảm thiểu thời gian phản ứng.",
      "Đừng để bị phân tâm bởi độ dài của con số.",
    ],
  ),
  "odd_one_out": (
    objective: "Hãy nhận ra một vật không có chung đặc điểm.",
    controls: "Hãy lấy vật lạ ra khỏi mạng lưới.",
    walkthrough: [
      "Quét chuỗi các hình, biểu tượng hoặc ảnh.",
      "Xác định mẫu hoặc quy tắc mà phần đông họ theo.",
      "Tìm một món đồ phá vỡ quy tắc này.",
      "Trước khi hết thời gian, hãy gõ vào cái bình động mạch chủ.",
    ],
    strategies: [
      "Tìm sự khác biệt về màu sắc, hình dạng, định hướng hoặc kích cỡ.",
      "Quét có hệ thống (ví dụ, hàng từng hàng) thay vì ngẫu nhiên.",
      "Nếu nó là một mạng lưới các kí tự tương tự (như 'O' và '0'), không tập trung đôi mắt của bạn một chút để làm cho một kỳ lạ bật.",
    ],
  ),
  "odd_rotation": (
    objective: "Tìm đối tượng mà là một phiên bản đã được phản ánh, không chỉ là một phiên bản quay, của những người khác.",
    controls: "Gõ vào đối tượng không thể xoay để phù hợp với hình dạng đích.",
    walkthrough: [
      "Quan sát hình tham chiếu và nhiều lựa chọn.",
      "xoay tâm trí mỗi lựa chọn để phù hợp với hình tham chiếu.",
      "Xác định hình nào cần lật (rroring) thay vì quay.",
      "Đánh vào hình dạng không đối xứng, phản chiếu.",
    ],
    strategies: [
      "Chọn một điểm cụ thể hoặc tính năng đối xứng trên hình và theo dõi hướng của nó.",
      "Xác định \"tay\" (bên trái hoặc bên phải) của các đối tượng.",
      "Quay trong tâm trí các hình dạng với 90 độ tăng dần.",
    ],
  ),
  "one_letter_shift": (
    objective: "Biến từ này thành từ khác bằng cách thay đổi chính xác từng chữ cái một, tạo ra những từ hợp lệ tại mỗi bước.",
    controls: "Dùng bàn phím để gõ từ hợp lệ kế tiếp trong chuỗi.",
    walkthrough: [
      "Hãy nhìn từ bắt đầu và từ cuối cùng của mục tiêu.",
      "Xác định một chữ cái bạn có thể thay đổi để tạo ra một từ điển hợp lệ mới.",
      "Nhập chữ mới.",
      "Lặp lại tiến trình cho đến khi bạn đạt được từ đích.",
    ],
    strategies: [
      "Làm việc từ cả hai đầu; suy nghĩ về từ ngữ cách xa mục tiêu.",
      "Từ điển thường dễ dàng nhất để thay đổi để tạo ra từ mới.",
      "Đừng lo lắng nếu con đường của bạn không ngắn nhất, miễn là mỗi bước chân là một từ thực sự.",
    ],
  ),
  "operation_span": (
    objective: "Giải quyết các vấn đề toán học đơn giản trong khi đồng thời nhớ một chuỗi các chữ cái hoặc từ ngữ.",
    controls: "Đáp ứng True/False cho phương trình toán học, sau đó nhập chuỗi nhớ ở cuối.",
    walkthrough: [
      "Một phương trình sẽ xuất hiện; xác định nó đúng hay sai.",
      "Ngay sau đó, một lá thư hoặc một từ sẽ hiện ra một thời gian ngắn.",
      "lặp lại quá trình thay đổi này cho một vài vòng.",
      "Ở màn hình thu hồi, hãy gõ vào tất cả các chữ cái/từ ngữ mà bạn nhớ theo thứ tự chính xác của chúng.",
    ],
    strategies: [
      "Giải quyết bài toán càng nhanh càng tốt để có thêm thời gian để luyện tập trình tự bộ nhớ.",
      "Sử dụng từ viết tắt hoặc làm cho một câu chuyện từ chữ/từ để ghi nhớ chúng.",
      "Hãy nói lớn lên trong đầu bạn liên tục.",
    ],
  ),
  "orbit_tap": (
    objective: "Ấn vào màn hình chính xác khi một vật thể di chuyển thẳng hàng với vùng mục tiêu trên quỹ đạo của nó.",
    controls: "Đánh vào mọi nơi trên màn hình để khởi động hành động.",
    walkthrough: [
      "Xem vật thể di chuyển theo quỹ đạo.",
      "Lưu ý vị trí của mục tiêu văn phòng.",
      "Dự đoán tốc độ và quỹ đạo của vật thể.",
      "Mở màn hình chính xác khi đối tượng chồng lên nhau.",
    ],
    strategies: [
      "Tập trung vào mục tiêu, không phải đối tượng di chuyển.",
      "Học nhịp điệu và tốc độ của quỹ đạo.",
      "Giải thích cho phản ứng thời gian của bạn bằng cách gõ nhẹ trước khi hoàn toàn thẳng hàng.",
    ],
  ),
  "oxymoron_hunt": (
    objective: "Hãy xác định danh sách các cụm từ có những cụm từ mâu thuẫn nhau.",
    controls: "Hãy gõ vào cụm từ tạo thành một máy tạo oxy.",
    walkthrough: [
      "Đọc kỹ tất cả các cụm từ được cung cấp.",
      "Hãy tìm hai cụm từ liên tiếp hoặc sát nhau có nghĩa ngược lại.",
      "Bỏ các cụm từ mô tả thông thường.",
      "Gõ vào câu mâu thuẫn (ví dụ, 'làm cho im lặng' để ghi điểm.",
    ],
    strategies: [
      "Tìm kiếm tính từ cực đoan kết hợp với danh từ cực đoan.",
      "Hãy đọc ý nghĩa thật sự của mỗi từ một cách độc lập để nhận ra sự mâu thuẫn.",
      "Làm quen với những con tôm ô-xy thông thường như tômjumbo hay 'rất ngon'.",
    ],
  ),
  "palindrome_builder": (
    objective: "Xây dựng một tấm bảng hợp lệ (một từ đọc cùng dòng và ngược lại) dùng những mảnh chữ.",
    controls: "Gõ hoặc kéo thư vào đúng vị trí để tạo ra từ.",
    walkthrough: [
      "Xem lại các miếng chữ cái sẵn có.",
      "Nhận diện cặp chữ cái giống hệt nhau, vì chúng phải phản chiếu nhau.",
      "Đặt chữ đơn (nếu có) ở chính giữa.",
      "Sắp xếp các cặp còn lại một cách cân xứng để đánh vần một từ hợp lệ.",
    ],
    strategies: [
      "Luôn luôn tìm thấy các chữ giữa đầu tiên nếu từ dài là lẻ.",
      "Làm việc từ bên ngoài, đặt những tiền tố thông thường và hậu tố phản chiếu của chúng.",
      "Bảo đảm rằng chuỗi kết quả thực sự đánh vần một từ thật sự trong từ điển.",
    ],
  ),
  "pangram_sprint": (
    objective: "Xác định những chữ cái bị mất hoặc lắp đặt một đoạn pangram (một câu chứa mỗi chữ cái của bảng chữ cái).",
    controls: "Gõ các chữ cái bị mất hoặc kéo các từ vào thứ tự.",
    walkthrough: [
      "Đọc câu không đầy đủ được cung cấp trên màn hình.",
      "Xác định chữ cái nào chưa được dùng.",
      "Trích dẫn từ ngữ còn thiếu dùng chính xác những chữ còn lại.",
      "Nhập từ đúng để hoàn thành pangram.",
    ],
    strategies: [
      "Giữ bảng kiểm tra trí óc về những chữ cái hiếm như Q, X, Z và J.",
      "Dùng các manh mối ngữ pháp và ngữ cảnh để tìm ra loại từ nào còn thiếu.",
      "Hãy nhớ những hình chữ cái cổ điển như \"Con cáo nâu nhanh chóng nhảy qua con chó lười biếng.\"",
    ],
  ),
  "paper_folding": (
    objective: "Xác định mẫu lỗ cuối cùng sau khi một mảnh giấy gấp và được mở ra.",
    controls: "Gõ vào lưới kết quả chính xác trong 4 lựa chọn được cung cấp.",
    walkthrough: [
      "Quan sát trình tự gấp mà các mũi tên chỉ ra.",
      "Hãy lưu ý điểm nào gây ra cú đấm trên tờ giấy gấp.",
      "Tâm trí mở tờ giấy theo thứ tự đảo ngược.",
      "Chọn tùy chọn khớp với mẫu lỗ đã hình dung.",
    ],
    strategies: [
      "Theo dõi sự phản chiếu của cú đấm qua mỗi đường gấp.",
      "Loại bỏ những lựa chọn có lỗ hổng ở những nơi không tưởng.",
      "Hãy nhớ rằng gấp chéo trao đổi tọa độ X và Y.",
    ],
  ),
  "path_finder": (
    objective: "Theo một đường đi liên tục của một chiều dài cụ thể từ điểm đầu đến điểm thoát mà không chồng chéo.",
    controls: "Kéo ngón tay qua lưới để vẽ đường dẫn từ đầu đến cuối.",
    walkthrough: [
      "Xác định điểm đầu (S) và thoát (E) trên lưới.",
      "Hãy lưu ý đến độ dài cần thiết được cung cấp theo gợi ý này.",
      "Kéo qua các tế bào lưới để tạo một đường chính xác chiều dài.",
      "Kết nối đường dẫn đến điểm thoát để hoàn tất cấp.",
    ],
    strategies: [
      "Nếu bạn đến được lối thoát quá sớm, bạn cần phải tìm một con đường quanh co hơn.",
      "Theo dõi số bước khi bạn kéo.",
      "Làm việc ngược từ lối ra để tìm đoạn đường dẫn hợp lệ.",
    ],
  ),
  "path_intersect": (
    objective: "Xác định tọa độ lưới chính xác nơi hai đường chồng chéo nhau giao nhau.",
    controls: "Gõ vào các tế bào cụ thể trên mạng lưới nơi các con đường gặp nhau.",
    walkthrough: [
      "Quan sát hai con đường màu vẽ trên màn hình.",
      "Theo dõi quỹ đạo của cả hai con đường.",
      "Xác định một tế bào mà chúng chồng lên nhau.",
      "Nhấn nút giao lộ để xác minh câu trả lời.",
    ],
    strategies: [
      "Tập trung vào khu vực chung nơi các đoạn ngang và thẳng đứng gặp nhau.",
      "Theo dõi một con đường với đôi mắt của bạn và tìm kiếm sự thay đổi màu sắc của con kia.",
      "Đừng vội; hãy xác nhận hình vuông này thẳng hàng với cả hai đường dẫn.",
    ],
  ),
  "path_recall": (
    objective: "Hãy nhớ một con đường hiển thị ngắn trên một mạng lưới và tái tạo chính xác từ bộ nhớ.",
    controls: "Đập các tế bào lưới theo đúng trình tự để tái tạo đường đi.",
    walkthrough: [
      "Cẩn thận xem xét đường đi được đánh dấu trên lưới điện.",
      "Chờ cho con đường biến mất và lưới điện được dọn sạch.",
      "Gõ vào ô cửa của con đường được ghi nhớ.",
      "Tiếp tục gõ các tế bào bên cạnh để hoàn tất chuỗi.",
    ],
    strategies: [
      "Hãy hình dung con đường là một hình dạng riêng biệt thay vì bước đi riêng lẻ.",
      "Nhóm các hành động thành từng đoạn (ví dụ, 'hai phải, một lên'.",
      "Hãy nhìn vào lưới điện ngay cả khi nó an toàn để giữ bộ nhớ không gian.",
    ],
  ),
  "pattern_sequence_draw": (
    objective: "Quan sát một chuỗi các đường nối được vẽ giữa các nút và mô phỏng chính xác mẫu.",
    controls: "Kéo ngón tay của bạn để kết nối các nút theo thứ tự chính xác.",
    walkthrough: [
      "Xem các lõi ánh sáng và đường thẳng kết nối theo thứ tự cụ thể.",
      "Chờ cho giai đoạn vẽ hoàn thành.",
      "Bắt đầu từ nút đầu tiên và kéo để tái tạo kết nối.",
      "Phát hành sau khi kết nối cuối cùng để đệ trình mô hình của bạn.",
    ],
    strategies: [
      "Tập trung vào hình dạng hình học được hình thành bởi các đường thẳng.",
      "Hãy lần theo mẫu trên không bằng ngón tay của bạn.",
      "Hãy nhớ điểm đầu và cuối như điểm mũi neo.",
    ],
  ),
  "percentage_peak": (
    objective: "Tính toán hoặc ước tính phần trăm để xác định giá trị kết quả cao nhất giữa nhiều tùy chọn.",
    controls: "Gõ vào tùy chọn đại diện cho số lượng tính toán lớn nhất.",
    walkthrough: [
      "Đọc tỷ lệ phần trăm biểu hiện trên màn hình.",
      "Nhanh chóng ước lượng giá trị tuyệt đối của mỗi biểu thức.",
      "So sánh các giá trị tính toán.",
      "Gõ vào hộp có giá trị cao nhất.",
    ],
    strategies: [
      "Sử dụng ước tính (ví dụ, 50% là một nửa, 10% là di chuyển thập phân).",
      "Tìm kiếm những kẻ thấp kém và lờ chúng đi.",
      "Tập trung vào kích thước cơ bản nếu tỷ lệ phần trăm giống nhau.",
    ],
  ),
  "percentage_shopping": (
    objective: "Tính toán giá cuối cùng của mục bằng cách áp dụng đúng phần trăm giảm giá hoặc đánh dấu.",
    controls: "Chọn giá cuối cùng chính xác từ các tùy chọn được cung cấp.",
    walkthrough: [
      "Hãy lưu ý giá gốc của món hàng và tỷ lệ chiết khấu.",
      "Tính toán lượng chiết khấu bằng cách áp dụng tỷ lệ phần trăm.",
      "Giảm giá từ giá gốc.",
      "Gõ tùy chọn tương đương với giá cuối cùng tính toán của bạn.",
    ],
    strategies: [
      "Với 20%, tính toán 10% và nhân đôi, rồi trừ đi.",
      "Thay vào đó, tính toán trực tiếp 80% giá gốc.",
      "Số vòng để đánh giá nhanh nếu tùy chọn ở xa.",
    ],
  ),
  "peripheral_focus": (
    objective: "Giữ cho trọng tâm tập trung ổn định trong khi nhanh chóng xác định mục tiêu xuất hiện trong tầm nhìn ngoại biên của bạn.",
    controls: "Mở màn hình ở góc phần tư nơi mục tiêu xuất hiện.",
    walkthrough: [
      "Tập trung mắt vào điểm tập trung.",
      "Chờ hình thù mục tiêu xuất hiện ngắn trên các cạnh.",
      "Gõ vào vùng tương ứng trên màn hình trước khi mục tiêu biến mất.",
      "Tiếp tục tập trung vào mục tiêu tiếp theo.",
    ],
    strategies: [
      "Đừng rời mắt khỏi trung tâm; hãy tin cậy thị lực ngoại vi của bạn.",
      "Hãy tập trung một chút để mở rộng tầm nhìn.",
      "Phản ứng nhanh khi thời gian thuyết trình giảm đi với mức độ cao hơn.",
    ],
  ),
  "perspective_shift_view": (
    objective: "Xác định cấu trúc khối 3D trông như thế nào khi nhìn từ một góc khác nhau.",
    controls: "Đánh vào hình chiếu 2D phù hợp với góc nhìn đã yêu cầu.",
    walkthrough: [
      "Kiểm tra cấu trúc khối ba chiều được hiển thị ở trung tâm.",
      "Xin lưu ý hướng xem đã yêu cầu (ví dụ, Top, Trái, Mặt trận).",
      "Quay tâm trí đối tượng để đối mặt với hướng đó.",
      "Chọn bóng 2 chiều tương ứng từ các tùy chọn.",
    ],
    strategies: [
      "Đếm chiều cao tối đa hay chiều rộng khối để loại trừ các tùy chọn sai.",
      "Tìm những đặc điểm khác nhau như khoảng cách hoặc những khối.",
      "Hãy hình dung bạn đang đứng bên cạnh đối tượng.",
    ],
  ),
  "perspective_taking": (
    objective: "Xác định bố trí trái/phải từ góc nhìn của hình nhân trong cảnh.",
    controls: "Chọn hướng đúng hoặc bố trí đối tượng dựa trên góc nhìn của Avatar.",
    walkthrough: [
      "Quan sát vị trí của Avatar và hướng mà họ đang đối mặt.",
      "Lưu ý đối tượng mục tiêu liên quan đến Avatar.",
      "tinh thần bước vào giày của Avatar để xác định bên trái hay bên phải.",
      "Gõ đúng câu trả lời.",
    ],
    strategies: [
      "Nếu Avatar đối mặt với anh, thì hai bên trái và phải của họ đối diện với anh.",
      "Dùng các dấu hiệu vật lý như quay cơ thể hoặc đầu một chút để giúp hình dung.",
      "Tập trung vào bàn tay của Avatar hay định hướng.",
    ],
  ),
  "phonetic_guess": (
    objective: "Giải mã từ tiếng Anh chính xác dựa trên chính tả ngữ âm hoặc cách phát âm.",
    controls: "Gõ hay chọn từ đúng.",
    walkthrough: [
      "Đọc chính tả ngữ âm trên màn hình.",
      "Nếu cần, hãy nói lớn tiếng.",
      "Xác định từ tiếng Anh tiêu chuẩn mà nó đại diện.",
      "Hãy nhập câu trả lời của bạn để tiếp tục.",
    ],
    strategies: [
      "Nói lớn tiếng từ này nhanh chóng giúp vượt qua sự nhầm lẫn về chính tả thị giác.",
      "Tập trung vào các âm nguyên âm vì chúng thường là những manh mối lớn nhất.",
      "Đừng suy nghĩ quá nhiều về những chữ cái im lặng bị thiếu trong cách đánh vần ngữ âm.",
    ],
  ),
  "pipes": (
    objective: "Xoay đoạn ống để tạo ra dòng chảy liên tục, không bị phá vỡ từ điểm đầu đến điểm cuối.",
    controls: "Gõ vào từng mảnh ống để xoay 90 độ theo chiều kim đồng hồ.",
    walkthrough: [
      "Xác định điểm đầu và điểm cuối của đường ống.",
      "Các mảnh đập thẳng vào các miếng cạnh nhau.",
      "Kết nối tất cả các đoạn",
      "Hoàn tất kết nối để cho chất lỏng chảy và hoàn tất cấp độ.",
    ],
    strategies: [
      "Bắt đầu từ các cạnh hoặc cố định điểm và làm việc theo cách của bạn bên trong.",
      "Tìm những góc và những mảnh thẳng chỉ vừa với một cách hợp lý.",
      "Tránh tạo ra những vòng lặp khép kín mà không kết nối với dòng chính.",
    ],
  ),
  "pixel_mimic": (
    objective: "Tạo lại một mô hình nghệ thuật điểm ảnh cụ thể trên một mạng lưới trống.",
    controls: "Tế bào đục trên mạng lưới của bạn để đổi màu của chúng để phù hợp với mục tiêu.",
    walkthrough: [
      "Nghiên cứu mẫu điểm ảnh đích được hiển thị ở đầu trang.",
      "Gõ các ô tương ứng vào lưới rỗng bên dưới.",
      "Kiểm tra các ô vuông màu trùng với mục tiêu.",
      "Hoàn tất mẫu để kích hoạt điều kiện chiến thắng.",
    ],
    strategies: [
      "Làm việc hàng hay cột theo hàng để tránh những điểm ảnh còn thiếu.",
      "Dùng các cạnh và góc làm điểm tham khảo.",
      "Đếm khoảng trống giữa điểm ảnh để định vị chính xác.",
    ],
  ),
  "portmanteau_split": (
    objective: "Hãy xác định hai từ gốc được kết hợp với nhau để tạo thành từ điển của người Do Thái.",
    controls: "Hãy chọn hai từ đúng trong danh sách đã cung cấp.",
    walkthrough: [
      "Đọc từ điển thành ngữ cho trước (ví dụ, 'Bruch').",
      "Phân tích từ để tìm các thành phần hòa hợp.",
      "Chọn từ gốc đầu tiên (ví dụ, 'G'.",
      "Chọn từ gốc thứ hai (ví dụ, 'Lnluch') cần phục tùng.",
    ],
    strategies: [
      "Hãy nhìn vào sự khởi đầu và kết thúc của từ cho các mảnh rễ.",
      "Hãy nghĩ về định nghĩa của bến cảng để tìm ra rễ cây.",
      "Sử dụng một quá trình loại trừ nếu các tùy chọn là khó khăn.",
    ],
  ),
  "prime_factor_trees": (
    objective: "Hãy chia con số tổng hợp thành những yếu tố chính của nó bằng cách hoàn tất biểu đồ nhánh cây.",
    controls: "Gõ nút rỗng và chọn các yếu tố số nguyên tố chính xác.",
    walkthrough: [
      "Hãy nhìn con số chính trên ngọn cây.",
      "Tìm hai số nhân để làm cho con số đó.",
      "Tiếp tục phá vỡ số lượng tổng hợp cho đến khi chỉ còn số nguyên tố.",
      "Điền đầy tất cả các nút đúng cách để kết thúc cái cây.",
    ],
    strategies: [
      "Luôn luôn kiểm tra xem một số chia hết cho 2 hay 3 trước.",
      "Hãy nhớ rằng các nhánh phải nhân với nhau để tương đương với các nút phía trên.",
      "Chỉ có số nguyên tố thuộc về các nút ở dưới cùng.",
    ],
  ),
  "prime_hunter": (
    objective: "Xác định và chọn tất cả các số nguyên tố từ một lưới trước khi đồng hồ hẹn giờ hết.",
    controls: "Hãy gõ những con số mà anh tin là số nguyên tố để thu thập chúng.",
    walkthrough: [
      "Quét lưới các con số trình bày.",
      "Xác định những con số chia hết cho 1 và bản thân.",
      "Ghi điểm nhanh lên.",
      "Tránh pha trộn số lượng, là điều sẽ dẫn đến một hình phạt.",
    ],
    strategies: [
      "Ghi nhớ số nguyên tố lên đến 100 cho tốc độ.",
      "Nhanh chóng loại bỏ các số chẵn (trừ 2) và số kết thúc trong 5.",
      "Kiểm tra khả năng xác thực của 3 chữ số để nhanh chóng loại trừ tổng hợp.",
    ],
  ),
  "quick_math": (
    objective: "Giải quyết một loạt các phương trình số học cơ bản càng nhanh càng tốt.",
    controls: "Gõ chính xác câu trả lời từ các lựa chọn hoặc dùng bàn phím để gõ nó.",
    walkthrough: [
      "Một phương trình xuất hiện trên màn hình.",
      "Thực hiện tính toán trong đầu một cách nhanh chóng.",
      "Nhập hoặc chọn câu trả lời đúng.",
      "Di chuyển ngay đến phương trình tiếp theo để tối đa hóa điểm của bạn.",
    ],
    strategies: [
      "Dựa vào các bước tắt của toán học tinh thần và học thuộc lòng.",
      "Đối với nhiều lựa chọn, sử dụng tính toán để ngay lập tức loại bỏ các câu trả lời sai.",
      "Giữ một nhịp độ ổn định; đừng hoảng sợ nếu bạn bỏ lỡ một nhịp.",
    ],
  ),
  "radical_roots": (
    objective: "Tính toán hình vuông hoặc khối lập phương gốc của số cho trước, hoặc đơn giản là biểu thức cấp tiến.",
    controls: "Chọn câu trả lời đúng số hoặc đơn giản hóa hình thức từ các tùy chọn.",
    walkthrough: [
      "Đọc cách diễn đạt tận gốc được hiển thị trên màn hình.",
      "Xác định giá trị gốc hoặc đơn giản hóa biểu thức.",
      "Hãy so sánh kết quả của bạn với những lựa chọn được cung cấp.",
      "Gõ đúng lựa chọn để tiến lên.",
    ],
    strategies: [
      "Ghi nhớ các ô vuông hoàn hảo phổ biến (1-44) và các khối lập phương hoàn hảo (1-25).",
      "Để đơn giản hóa, tìm yếu tố hình vuông hoàn hảo lớn nhất bên trong gốc.",
      "Sử dụng số cuối cùng của số để ước tính gốc.",
    ],
  ),
  "reading_span": (
    objective: "Đọc các câu, xác định giá trị hợp lý của mỗi câu và nhớ từ cuối cùng của mỗi câu.",
    controls: "Gõ True/False cho các câu, rồi chọn các từ đã ghi nhớ theo thứ tự.",
    walkthrough: [
      "Đọc câu trình bày và gõ đúng nếu nó hợp lý, nếu nó không đúng.",
      "Hãy ghi nhớ từ cuối cùng của câu đó.",
      "lặp lại quá trình này cho toàn bộ chuỗi các câu.",
      "Ở cuối, hãy chọn những từ cuối cùng đã ghi nhớ theo thứ tự chính xác khi chúng xuất hiện.",
    ],
    strategies: [
      "Tạo ra một câu chuyện tinh thần hoặc từ viết tắt bằng những từ cuối để giúp bộ nhớ.",
      "Đừng để quyết định True/False đánh lạc hướng anh khỏi việc lưu trữ từ đó.",
      "Tập lại danh sách các từ trong nội bộ giữa các câu.",
    ],
  ),
  "reflex_tap": (
    objective: "Kiểm tra thời gian phản ứng của bạn bằng cách gõ vào màn hình ngay khi có một tín hiệu trực quan cụ thể xuất hiện.",
    controls: "Đập bất cứ nơi nào trên màn hình nhanh nhất có thể khi được nhắc.",
    walkthrough: [
      "Đợi màn hình hay chỉ thị thay đổi màu/ đường.",
      "Giữ ngón tay bay lượn trên màn hình.",
      "Gõ ngay khi có tín hiệu.",
      "Tránh xâm nhập sớm để ngăn chặn hình phạt bắt đầu sai lầm.",
    ],
    strategies: [
      "Tập trung mạnh mẽ vào trung tâm của màn hình để giảm thiểu thời gian xử lý.",
      "Giữ ngón tay vỗ nhẹ nhàng nhưng sẵn sàng di chuyển.",
      "Đừng dự đoán thời điểm; chỉ phản ứng trước sự thay đổi thị giác.",
    ],
  ),
  "relational_memory": (
    objective: "Hãy nhớ những cặp hoặc mối quan hệ cụ thể giữa các món đồ được trình bày.",
    controls: "Đánh trúng mục đã hoàn thành khi được nhắc.",
    walkthrough: [
      "Quan sát một loạt các mục có cặp (ví dụ, một đối tượng cụ thể ở một địa điểm cụ thể).",
      "Tập trung vào việc mã hóa liên kết giữa hai mục.",
      "Trong giai đoạn thu hồi, một món đồ của một cặp sẽ được trình bày.",
      "Chọn mục tương ứng trong các tùy chọn.",
    ],
    strategies: [
      "Tạo ra những hình ảnh tinh thần sống động, kì lạ liên kết hai vật với nhau.",
      "Nói lớn lên một câu để củng cố trí nhớ.",
      "Chú ý đến những chi tiết độc đáo của những thứ trông giống nhau.",
    ],
  ),
  "reverse_stroop": (
    objective: "Hãy nhận diện chính chữ viết, đồng thời lờ đi màu mực mâu thuẫn được in.",
    controls: "Ấn nút tương ứng với chữ, không phải màu.",
    walkthrough: [
      "Một từ màu (ví dụ, « GỢI Ý » xuất hiện trên màn hình với màu mực khác (ví dụ, mực đỏ).",
      "Hãy nén lại sự thôi thúc chọn màu mực.",
      "Đọc văn bản.",
      "Gõ tùy chọn khớp với văn bản đã ghi.",
    ],
    strategies: [
      "Tập trung hơi kém tập trung hoặc nháy mắt để làm mờ màu trong khi đọc.",
      "Âm thanh âm thanh âm thanh ra các chữ cái để củng cố việc đọc trên nhận thức màu sắc.",
      "Giữ tốc độ ổn định để tránh rơi vào cái bẫy màu sắc.",
    ],
  ),
  "rhyme_master": (
    objective: "Xác định từ vần với từ đích được đưa ra từ lựa chọn.",
    controls: "Hãy gõ vào từ vần với mục tiêu.",
    walkthrough: [
      "Đọc từ đích ở đầu màn hình.",
      "Đọc các lựa chọn được cung cấp.",
      "phát âm thanh để tìm âm thanh kết thúc âm thanh âm thanh.",
      "Chọn từ khớp chính xác cần ghi.",
    ],
    strategies: [
      "Bỏ qua chính tả; tập trung hoàn toàn vào âm thanh ngữ âm thanh (ví dụ, 'g' và 'late').",
      "Nói lớn tiếng từ mục tiêu và các tùy chọn trong đầu.",
      "Hãy coi chừng những cái ống gần gũi được thiết kế để lừa anh.",
    ],
  ),
  "rhythm_master": (
    objective: "Lắng nghe một chu trình nhịp điệu và đập nó lại với thời điểm chính xác.",
    controls: "Nhấn nút đã chọn đồng bộ với nhịp điệu nhớ.",
    walkthrough: [
      "lắng nghe kỹ giai điệu thính giác được chơi.",
      "Xem các chỉ số hình ảnh nếu có thể nắm được thời điểm.",
      "Khi nhắc, hãy gõ vào màn hình để sao chép nhịp đập.",
      "Duy trì tốc độ chính xác và tạm dừng của chuỗi gốc.",
    ],
    strategies: [
      "Đánh vào chân hoặc gật đầu để nội bộ nhịp đập trong khi lắng nghe.",
      "Chia ra từng nhịp trong đầu để xử lý các cú gõ.",
      "Đừng vội, giữ máy nhịp tim bên trong ổn định là chìa khóa.",
    ],
  ),
  "roman_arithmetic": (
    objective: "Các vấn đề số học được giải quyết hoàn toàn bằng chữ số La Mã.",
    controls: "Hãy gõ vào câu trả lời chính xác của người La Mã từ những lựa chọn được đưa ra.",
    walkthrough: [
      "Đọc phương trình toán học bằng số La Mã.",
      "Chuyển đổi chữ số thành số chuẩn trong đầu.",
      "Thực hiện phép cộng, phép trừ, hay phép nhân.",
      "Chuyển đổi kết quả thành số La Mã và chọn nó.",
    ],
    strategies: [
      "Ghi nhớ các giá trị khóa: I = 1, V = 5, X = 10, L = 50, C = 100.",
      "Coi chừng trừ ký hiệu (ví dụ, IV = 4, IX = 9).",
      "Làm toán ở cơ số 10 đầu tiên để tránh lỗi.",
    ],
  ),
  "room_inspector": (
    objective: "Ghi nhớ bố trí và vật thể trong một căn phòng, sau đó xác định những gì đã thay đổi sau một giai đoạn chuyển tiếp ngắn.",
    controls: "Gõ vào những vật đã được thêm vào, gỡ bỏ, hoặc thay đổi.",
    walkthrough: [
      "quét phòng cẩn thận trong giai đoạn quan sát.",
      "Hãy ghi nhớ vị trí, màu sắc và sự hiện diện của đối tượng.",
      "Chờ màn hình chớp hay chuyển đổi.",
      "Kiểm tra tình trạng phòng mới và chạm vào sự khác biệt.",
    ],
    strategies: [
      "Quét phòng một cách có hệ thống (ví dụ, từ trái sang phải, từ trên xuống dưới).",
      "Đếm số đồ vật trên kệ hoặc bàn.",
      "Tập trung vào những đối tượng nổi tiếng mà rất có thể là những ứng cử viên để thay đổi.",
    ],
  ),
  "rotating_maze": (
    objective: "Chuyển một quả bóng qua một mê cung đến lối ra bằng cách xoay toàn bộ cấu trúc mê cung.",
    controls: "Nhấn nút quay trái hoặc phải (hoặc kéo) để nghiêng mê cung.",
    walkthrough: [
      "quan sát vị trí hiện tại của quả bóng và vị trí của lối ra.",
      "Lên đường qua hành lang.",
      "Xoay mê cung để trọng lực kéo quả bóng theo kế hoạch.",
      "Bắt bóng trên tường để tránh nó rơi vào bẫy hoặc ngõ cụt.",
    ],
    strategies: [
      "Hãy nghĩ một bước trước về nơi quả bóng sẽ hạ cánh sau khi quay.",
      "Dùng những vòng xoay nhỏ, có kiểm soát thay vì quay cuồng.",
      "Dùng góc để chặn quả bóng trong khi anh định hướng lại mê cung.",
    ],
  ),
  "rule_switcher": (
    objective: "Sắp xếp các mục dựa trên quy tắc thay đổi động (ví dụ, sắp xếp theo màu, rồi chuyển đổi thành hình).",
    controls: "Gõ vào chồng đích chính xác dựa trên quy tắc hoạt động hiện thời.",
    walkthrough: [
      "Xem quy tắc sắp xếp được hiển thị trên màn hình.",
      "Xem xét mục hiện thời cần được sắp xếp.",
      "Gõ vào chồng tương ứng khớp với quy tắc.",
      "Chú ý kỹ khi quy tắc thay đổi ngẫu nhiên và thích nghi ngay lập tức.",
    ],
    strategies: [
      "Tiếp tục lặp lại quy tắc hoạt động trong đầu (ví dụ, « Màu, màu, màu »).",
      "Khi quy tắc chuyển đổi, hãy dừng lại một chút để khởi động lại trạng thái tinh thần của bạn.",
      "Đừng phụ thuộc vào bộ nhớ cơ bắp, đánh giá từng món đồ một.",
    ],
  ),
  "running_memory_span": (
    objective: "Hãy nhớ lại những thứ N cuối cùng của một chuỗi sau khi bài thuyết trình kết thúc.",
    controls: "Hãy gõ các mục theo thứ tự chúng được trình bày ở cuối chuỗi.",
    walkthrough: [
      "Xem chuỗi các mục được trình bày từng mục một.",
      "Hãy lưu ý rằng trình tự này có thể dừng lại bất cứ lúc nào.",
      "Khi chuỗi kết thúc, hãy gõ các mục tương ứng với mục N cuối cùng.",
      "Hãy nhớ lại họ theo đúng thứ tự mà họ đã xuất hiện.",
    ],
    strategies: [
      "Liên tục cập nhật trí nhớ của bạn với những mục gần đây nhất.",
      "Tập trung vào mục tiêu hiện tại trong tâm trí bạn khi có những mục mới xuất hiện.",
      "Tập trung vào trình tự, như bạn sẽ không biết khi nào nó kết thúc.",
    ],
  ),
  "schulte_table": (
    objective: "Tìm và dò tất cả các con số trong lưới theo thứ tự tăng càng nhanh càng tốt.",
    controls: "Theo thứ tự, bắt đầu từ 1.",
    walkthrough: [
      "một lưới 5x5 của số ngẫu nhiên (1-25) được trình bày.",
      "Tìm và gõ số 1.",
      "Tiếp tục tìm kiếm và gõ các con số theo thứ tự tăng dần (, 3, 4...).",
      "Hoàn tất lưới trong thời gian ngắn nhất có thể.",
    ],
    strategies: [
      "Tập trung vào trung tâm của lưới điện.",
      "Sử dụng tầm nhìn ngoại biên của bạn để xác định vị trí những con số tiếp theo.",
      "Cố gắng nhận ra số tiếp theo trong khi di chuyển ngón tay của bạn tới số hiện có.",
    ],
  ),
  "sdmt": (
    objective: "Khớp con số chính xác với biểu tượng trình bày dựa trên chìa khóa cung cấp trong giới hạn thời gian.",
    controls: "Hãy gõ số điện thoại trên cái numpad tương ứng với biểu tượng được trưng bày.",
    walkthrough: [
      "Xem lại chìa khóa tại các cặp bên trên cùng biểu tượng với số 1-9.",
      "Hãy nhìn vào biểu tượng lớn được trình bày ở trung tâm.",
      "Tìm số tương ứng của nó trong phím.",
      "Gõ số khớp trên bàn phím càng nhanh càng tốt.",
    ],
    strategies: [
      "Ghi nhớ những cặp ký hiệu thường xuyên nhất để tiết kiệm thời gian.",
      "Hãy nhìn vào biểu tượng và chìa khóa mục tiêu, và dựa vào bộ nhớ cơ cho bàn phím.",
      "Giữ nhịp độ ổn định để tối đa hóa điểm số.",
    ],
  ),
  "semantic_association": (
    objective: "Xác định từ liên quan chặt chẽ nhất với từ mục tiêu được đưa ra.",
    controls: "Gõ vào tùy chọn từ để tạo ra sự kết nối ngữ pháp mạnh nhất.",
    walkthrough: [
      "Đọc những từ hoặc khái niệm được đặt ra.",
      "Đánh giá các tùy chọn cho phép liên quan đến ngữ pháp.",
      "Chọn tùy chọn kết nối tốt nhất đến mục tiêu.",
      "Trả lời đúng hết mức có thể trong phạm vi giới hạn.",
    ],
    strategies: [
      "Tìm kiếm các loại hoặc các mối quan hệ chức năng.",
      "Loại bỏ các tùy chọn rõ ràng không liên quan trước.",
      "Hãy tin tưởng những mối quan hệ trước mắt của bạn.",
    ],
  ),
  "semantic_distance": (
    objective: "Không tìm thấy từ mục tiêu bí mật bằng cách đoán những từ liên quan và theo dõi khoảng cách ngữ nghĩa của chúng.",
    controls: "Hãy gõ từ ngữ của bạn vào hộp nhập rồi gửi hoặc bấm phím Enter.",
    walkthrough: [
      "Gõ bất kỳ từ đoán nào vào trường văn bản và gửi.",
      "Bạn có thể đoán lại điểm khoảng cách.",
      "Điểm thấp hơn có nghĩa là bạn gần với từ bí mật hơn.",
      "Hãy tham gia vào đồng nghĩa và các khái niệm liên hệ cho đến khi bạn tìm thấy từ bí mật (khoảng 0.0) trước khi thời gian hết hạn.",
    ],
    strategies: [
      "Bắt đầu với các từ miền rộng (tự nhiên, thực phẩm, không gian, mục) để nhận diện loại.",
      "Khi một đoán có điểm thấp (< 25), hãy kiểm tra những phần cụ thể, chức năng và kết hợp chặt chẽ với nhau.",
      "Điểm khoảng cách 0.0 cho thấy bạn đã tìm thấy từ bí mật thành công.",
    ],
  ),
  "semantic_link": (
    objective: "Lập thành một chuỗi các từ mà mỗi từ có liên hệ đầy ý nghĩa với từ trước.",
    controls: "Gõ vào từ logic tiếp theo trong trình tự từ các tùy chọn sẵn có.",
    walkthrough: [
      "Bắt đầu với từ đích ban đầu.",
      "Chọn từ trong các tùy chọn liên quan đến ngữ nghĩa.",
      "Từ được chọn trở thành mục tiêu mới.",
      "Tiếp tục xây dựng chuỗi hạt cho đến khi nó hoàn tất.",
    ],
    strategies: [
      "Hãy nghĩ một bước trước để đảm bảo rằng bạn không vẽ mình vào một góc.",
      "Bạn bè có thể bị phân loại, đồng nghĩa hoặc chức năng.",
      "Nếu bị mắc kẹt, hãy nhìn vào những lựa chọn còn lại để đảo ngược con đường.",
    ],
  ),
  "sentence_unscramble": (
    objective: "Sắp xếp lại những từ lộn xộn để tạo thành một câu văn đúng và đầy ý nghĩa.",
    controls: "Kéo và thả các từ vào đúng thứ tự, hoặc gõ chúng một cách ngẫu nhiên.",
    walkthrough: [
      "Đọc tất cả những từ lộn xộn được đưa ra trên màn hình.",
      "Xác định chủ đề, động từ, và đối tượng của câu.",
      "Sắp xếp từ ngữ theo đúng thứ tự quy ước.",
      "Gửi câu hoàn tất để xác minh tính chính xác.",
    ],
    strategies: [
      "Hãy tìm những từ được thủ công hóa để bắt đầu câu văn và chấm dứt nó.",
      "Nhóm các cụm từ phổ biến hoặc danh từ kết hợp với nhau trước.",
      "Hãy đọc lớn tiếng câu mà bạn đã hình thành trong đầu để kiểm tra dòng chảy tự nhiên.",
    ],
  ),
  "sequence_sleuth": (
    objective: "Xác định mẫu bên trong trong một chuỗi số hay biểu tượng và xác định phần tử còn thiếu.",
    controls: "Gõ hoặc nhập vào phần tử bị thiếu chính xác để hoàn thành chuỗi.",
    walkthrough: [
      "Kiểm tra chuỗi mục đã được cung cấp.",
      "Hãy xác định quy tắc điều khiển tiến trình (ví dụ, + 2, x3, một hình thay đổi).",
      "Tính giá trị bị thiếu dựa trên quy tắc này.",
      "Nhập câu trả lời đúng để giải câu đố.",
    ],
    strategies: [
      "Kiểm tra các khác biệt giữa các số kề bên trước.",
      "Nếu bổ sung đơn giản không hoạt động, hãy thử nhân hay thay đổi mẫu.",
      "Kiểm tra quy tắc giả định của anh chống lại tất cả các phần của chuỗi.",
    ],
  ),
  "sequence_stack": (
    objective: "Ghi nhớ và sao chép một chuỗi các vật thể phát triển mãi mãi.",
    controls: "Gõ các vật dụng theo đúng thứ tự mà chúng được hiển thị.",
    walkthrough: [
      "Xem chuỗi đầu của các mục.",
      "Tái tạo chuỗi bằng cách gõ lại các mục.",
      "Một mục mới được thêm vào cuối chuỗi.",
      "Tái tạo chuỗi mới kéo dài ngay từ đầu.",
    ],
    strategies: [
      "Nhóm các mục thành nhóm nhỏ (ví dụ, nhóm 3 hoặc 4).",
      "Tạo ra một ghi nhớ hoặc một đường dẫn không gian trong tâm trí bạn.",
      "Nói to hoặc trong đầu bạn khi nó đang chơi.",
    ],
  ),
  "shadow_pivot": (
    objective: "Xác định đối tượng ba chiều chính xác dựa trên bóng 2 chiều của nó.",
    controls: "Đánh dấu để xoay đối tượng hay gõ để chọn bóng tương ứng.",
    walkthrough: [
      "Hãy quan sát cái bóng 2 chiều chiếu trên tường.",
      "Kiểm tra các đối tượng 3D có sẵn.",
      "Hãy hình dung làm thế nào mỗi vật có thể tạo ra bóng từ nhiều góc độ khác nhau.",
      "Chọn đối tượng khớp hoàn hảo với bóng.",
    ],
    strategies: [
      "Tập trung vào các cạnh riêng biệt và các tính năng đối xứng của bóng.",
      "Quay các đối tượng trên trục X, Y và Z.",
      "Loại bỏ các lựa chọn mà có các tính năng bị mất hoàn toàn trong bóng.",
    ],
  ),
  "shape_shifter": (
    objective: "Theo dõi một hình dạng khi nó trải qua nhiều sự biến đổi và xác định kết quả cuối cùng.",
    controls: "Đánh đúng hình cuối cùng từ các lựa chọn cho trước.",
    walkthrough: [
      "Ghi nhớ hình ban đầu, màu và hướng",
      "Xem chuỗi các quy tắc chuyển đổi được áp dụng (ví dụ, xoay 90°, không đảo màu).",
      "Tâm trí áp dụng những biến đổi này từng bước một.",
      "Chọn kết quả cuối cùng từ những lựa chọn.",
    ],
    strategies: [
      "Cập nhật hình ảnh tinh thần của bạn về hình dạng sau mỗi biến đổi.",
      "Chú ý đến thứ tự hoạt động, vì nó ảnh hưởng đến tình trạng cuối cùng.",
      "Dùng ngón tay để theo dõi sự quay nếu việc hình dung khó khăn.",
    ],
  ),
  "shell_game": (
    objective: "Hãy nhìn vào thùng chứa giấu đối tượng trong khi chúng được xáo trộn nhanh chóng.",
    controls: "Gõ vào thùng hàng mà bạn tin rằng giữ được đối tượng khi chúng ngừng di chuyển.",
    walkthrough: [
      "Lưu ý vật chứa nào giữ đối tượng mục tiêu trước khi chúng bao phủ nó.",
      "Mắt bạn nhìn theo vật chứa cụ thể đó khi chúng xoay vòng.",
      "Đừng để những vật thể phân tâm phá vỡ sự tập trung của bạn.",
      "Gõ đúng container khi nó dừng lại.",
    ],
    strategies: [
      "Sửa mắt giữa hộp mục tiêu và giữa màn hình.",
      "Tránh chớp mắt trong lúc xáo trộn nhanh.",
      "Nếu theo dõi nhiều mục tiêu, hãy mở rộng tầm nhìn hơn là bắn vào mắt.",
    ],
  ),
  "shikaku": (
    objective: "Chia lưới thành hình chữ nhật để mỗi ô có chính xác một số, và diện tích bằng số đó.",
    controls: "Kéo qua các ô lưới để vẽ hình chữ nhật.",
    walkthrough: [
      "Hãy nhìn những con số rải rác khắp khu vực.",
      "Kéo để tạo hình chữ nhật xung quanh một số.",
      "Kiểm tra khu vực hình chữ nhật trùng khớp với con số.",
      "Điền đầy toàn bộ lưới bằng hình chữ nhật không lật.",
    ],
    strategies: [
      "Bắt đầu với số nguyên tố lớn, vì chúng chỉ có thể hình thành 1xN hoặc Nx1 hình chữ nhật.",
      "Tìm những con số bị mắc kẹt ở góc hay dọc theo các cạnh.",
      "Sử dụng suy luận: Nếu chỉ có thể đạt được một số cụ thể, hãy cho nó vào hình chữ nhật đó.",
    ],
  ),
  "silent_letter_search": (
    objective: "Xác định những từ chứa chữ yên lặng hoặc chỉ ra chữ yên lặng trong một từ.",
    controls: "Hãy gõ chữ bằng một lá thư thầm lặng, hoặc gõ vào chính chữ đó.",
    walkthrough: [
      "Phân tích từ hoặc danh sách các từ được trình bày.",
      "Phát âm từ trong đầu để kiểm tra chính tả ngữ âm.",
      "Xác định chữ viết nhưng không phát âm.",
      "Chọn lựa trước khi hết thời gian.",
    ],
    strategies: [
      "Coi chừng những tổ hợp chữ cái im lặng thông thường như 'kn', 'wr', 'm' và 'gh'.",
      "Hãy nhớ rằng 'e' ở cuối một từ thường im lặng và thay đổi các âm nguyên âm.",
      "Hãy thông báo kỹ lưỡng từ này để đảm bảo mọi chữ cái được liệt kê.",
    ],
  ),
  "silhouette_match": (
    objective: "Tìm cái bóng chính xác khớp với hình ảnh chi tiết.",
    controls: "Hãy gõ chính xác cái bóng từ các tùy chọn sẵn có.",
    walkthrough: [
      "Quan sát kỹ hình ảnh tham chiếu chi tiết.",
      "Hãy xem những lựa chọn có hình dạng như thế nào.",
      "Hãy lưu ý đến sự khác biệt tinh tế về tư thế, cạnh hoặc không gian tiêu cực.",
      "Chọn hình chính xác để tham chiếu.",
    ],
    strategies: [
      "Tập trung vào các cạnh và không gian tiêu cực hơn là trung tâm.",
      "Tìm những đặc điểm nhỏ, đặc biệt như ngón tay giơ lên, sợi tóc, hoặc cạnh không đều.",
      "Loại bỏ những hình ảnh rõ ràng không có đặc điểm nổi bật của bản gốc.",
    ],
  ),
  "silhouette_match_ortho": (
    objective: "Khớp hình chiếu chính xác (trên, trước, bên) với đối tượng 3D.",
    controls: "Đánh bại hình chiếu 2 chiều từ các lựa chọn.",
    walkthrough: [
      "Kiểm tra đối tượng 3 chiều và hướng xem đã yêu cầu (ví dụ, 'Top View').",
      "Tâm trí làm phẳng vật thể dọc theo trục đó.",
      "So sánh hình ảnh của bạn với lựa chọn 2D.",
      "Chọn hình chiếu phù hợp.",
    ],
    strategies: [
      "Bỏ qua toàn bộ chiều sâu; tưởng tượng nhìn vào đối tượng từ xa vô hạn.",
      "Hãy đếm số lượng các khối hay đoạn có thể nhìn thấy ở rìa ngoài.",
      "Coi chừng hình học ẩn có thể bị chặn bởi các phần tử cận cảnh.",
    ],
  ),
  "simon_command": (
    objective: "Chỉ làm theo chỉ dẫn khi có câu 'Simon nói'.",
    controls: "Nhấn nút hành động đúng, hoặc không được gõ nếu nó là trò lừa.",
    walkthrough: [
      "Đọc hoặc lắng nghe mệnh lệnh trên màn hình.",
      "Xem lệnh có bắt đầu bằng chữ ' Simon nói' không.",
      "Nếu có, hãy thực hiện nhanh hành động đã yêu cầu.",
      "Nếu không, hãy tuyệt đối không làm gì và chờ đợi.",
    ],
    strategies: [
      "Hãy rèn luyện bản thân để tìm câu gợi ý trước, trước khi thực hiện hành động.",
      "Hãy sẵn sàng nhưng kháng cự khuynh hướng hành động ngay lập tức.",
      "Hãy tập trung, vì nhịp độ sẽ tăng dần.",
    ],
  ),
  "simon_sequence": (
    objective: "Gregory",
    controls: "Đạp các nút màu theo đúng thứ tự.",
    walkthrough: [
      "Xem các nút chớp theo một trình tự cụ thể.",
      "Chờ cho trình tự kết thúc.",
      "Lặp lại trình tự bằng cách gõ các nút theo cùng thứ tự.",
      "Với mỗi vòng, một bước mới được thêm vào chuỗi.",
    ],
    strategies: [
      "Hãy sử dụng cả bộ nhớ thị giác lẫn thính giác; hãy phát âm âm thanh trong khi hình dung các màu sắc.",
      "Chỉ định số hoặc từ cho các màu sắc và lặp lại chúng trong đầu bạn.",
      "Tập hợp chuỗi số thành từng đoạn 3 hay 4 để dễ nhớ hơn.",
    ],
  ),
  "skyscrapers": (
    objective: "Đặt số 1 đến N trong lưới vì vậy không có số lặp lại trong bất kỳ hàng hoặc cột, trong khi thỏa mãn các đầu mối tầm nhìn.",
    controls: "Hãy gõ vào một điện thoại và chọn một số từ số điện thoại hoặc miếng đệm.",
    walkthrough: [
      "Hãy nhìn vào các đầu mối trên các cạnh của lưới chỉ ra bao nhiêu \"scrapers\" có thể nhìn thấy được.",
      "Những con số cao hơn chặn những con số nhỏ hơn phía sau.",
      "Điền vào lưới để mỗi hàng và cột có số 1- N mà không cần lặp lại.",
      "Hãy chắc chắn rằng mọi đầu mối đều thỏa mãn bởi độ cao được đặt.",
    ],
    strategies: [
      "Một gợi ý của '1' có nghĩa là tòa nhà cao nhất (n) phải được đặt ngay cạnh nó.",
      "Một manh mối của 'N' nghĩa là các tòa nhà phải theo thứ tự tăng dần từ cạnh đó.",
      "Dùng khả năng loại bỏ tương tự như Sudoku cho hàng và cột.",
    ],
  ),
  "slide_puzzle": (
    objective: "Sắp xếp lại các miếng trộn để tạo thành toàn bộ hình ảnh hoặc thứ tự số.",
    controls: "Gõ hoặc kéo một lát cạnh chỗ trống để trượt nó.",
    walkthrough: [
      "Kiểm tra lưới nhiễu và xác định vị trí chỉ có một khoảng trống.",
      "Trượt các mảnh vào khoảng trống để di chuyển chúng xung quanh.",
      "Cố gắng giải câu đố từng hàng, bắt đầu từ đầu.",
      "Đặt các mảnh cuối cùng ở góc dưới bên phải để hoàn thành câu đố.",
    ],
    strategies: [
      "Giải quyết hàng đầu và cột bên trái trước để giảm kích cỡ câu đố.",
      "Để trao đổi hai mảnh bên cạnh, bạn phải xoay chúng thành một vòng với khoảng trống.",
      "Hãy lên kế hoạch trước để tránh làm lộn xộn những phần đã được giải quyết xong.",
    ],
  ),
  "slitherlink": (
    objective: "Kết nối các dấu chấm nối với nhau tạo thành một vòng lặp liên tục duy nhất mà không cần băng qua hoặc nhánh.",
    controls: "Đánh vào các cạnh giữa các chấm để vẽ hoặc loại bỏ một đường thẳng.",
    walkthrough: [
      "nhìn vào những con số bên trong các tế bào.",
      "Con số này cho thấy chính xác có bao nhiêu cạnh là một phần của vòng thời gian.",
      "Vẽ đường thẳng để thỏa mãn mọi con số.",
      "Hãy đảm bảo các đường thẳng được đóng lại.",
    ],
    strategies: [
      "Một '0' có nghĩa là không có dòng nào có thể bao quanh nó; đánh dấu chúng với 'x' để loại bỏ chúng.",
      "Số 3 của Adjacent luôn có những đường song song ở rìa ngoài và một đường giữa chúng.",
      "Vòng thời gian không thể tự liên kết hoặc cắt ngang, điều này giúp cho các đường dẫn có sức ép hợp lý.",
    ],
  ),
  "sopt": (
    objective: "Chọn mục khác trong mỗi phiên chạy thử cho đến khi chọn xong mục.",
    controls: "Đánh cắp một món đồ từ lưới điện.",
    walkthrough: [
      "Một lưới các vật thể được hiển thị.",
      "Gõ bất cứ thứ gì anh muốn.",
      "Các vật thể xoay hoàn toàn vị trí của chúng.",
      "Nhấn vào một đối tượng chưa gõ xong. Lặp lại cho đến khi mọi đối tượng được chọn.",
    ],
    strategies: [
      "Hãy chọn một thứ tự không gian riêng (ví dụ, góc trên- trái tới bên phải) hoặc thứ tự phân loại.",
      "Ghi nhớ những mục bạn đã nhấp chuột bằng cách tạo ra một câu chuyện tâm thần.",
      "Đừng dựa vào bộ nhớ không gian, vì những thứ đó sẽ xáo trộn mọi lúc.",
    ],
  ),
  "source_monitoring": (
    objective: "Hãy nhớ không chỉ những thông tin đó, mà còn nhớ nguồn chính xác (ai, ở đâu, hay cách trình bày).",
    controls: "Gõ đúng nguồn tương ứng với mục đã trình bày.",
    walkthrough: [
      "Trong giai đoạn học tập, hãy quan sát các mục và lưu ý nguồn (ví dụ, hộp đỏ đấu với hộp xanh).",
      "Trong giai đoạn thử nghiệm, một món đồ được trình bày.",
      "Hãy nhớ lại nguồn liên quan đến món đồ ấy.",
      "Chọn đúng nguồn để ghi điểm.",
    ],
    strategies: [
      "Tạo một liên kết chặt chẽ giữa mục và nguồn của nó trong khi mã hóa.",
      "Cũng chú ý đến bối cảnh khi bạn làm cho chính nó.",
      "Dùng hình ảnh minh họa để hình dung đối tượng trong bối cảnh ban đầu.",
    ],
  ),
  "spatial_cabinet_memory": (
    objective: "Ghi nhớ vị trí của các vật thể khác nhau trong một mạng lưới hoặc nội các và nhớ lại chúng một cách chính xác.",
    controls: "Hãy gõ các khoang để tiết lộ hoặc đặt các vật thể dựa trên trí nhớ của bạn.",
    walkthrough: [
      "Quan sát nội các như các cánh cửa mở ra để tiết lộ các vật bên trong.",
      "Ghi nhớ đối tượng nào thuộc về khoang nào.",
      "Khi các cánh cửa đóng lại, bạn sẽ được nhắc phải tìm những vật cụ thể.",
      "Mở đúng ngăn để tiết lộ đối tượng đã yêu cầu.",
    ],
    strategies: [
      "Các đối tượng nhóm với nhau bằng hàng hoặc cột trong tâm trí bạn.",
      "Tạo một bản đồ tinh thần hoặc một câu chuyện kết nối các mục kề nhau.",
      "Tập trung vào bố trí chung hơn là nhìn chằm chằm vào một món đồ.",
    ],
  ),
  "spatial_conflict": (
    objective: "Hãy đáp lại sự hướng dẫn của mũi tên, đồng thời lờ đi vị trí mâu thuẫn không gian.",
    controls: "Ấn nút tương ứng với hướng mũi tên.",
    walkthrough: [
      "Một mũi tên sẽ xuất hiện trên màn hình.",
      "Lưu ý hướng mũi tên đang chỉ (bên phải hoặc bên phải).",
      "Bỏ qua phía nào hiển thị mũi tên.",
      "Nhanh chóng nhấn nút phù hợp với hướng mũi tên điểm.",
    ],
    strategies: [
      "Hãy tập trung nhìn vào đầu mũi tên để nhanh chóng xác định hướng đi.",
      "Cố gắng ngăn chặn sự thôi thúc của bạn để gõ vào bên mà sự kích thích xuất hiện.",
      "Hãy bình tĩnh và ưu tiên sự chính xác vượt quá tốc độ để tránh lỗi lầm.",
    ],
  ),
  "spelling_sprint": (
    objective: "Hãy nhanh chóng xác định xem từ này được viết đúng hay sai.",
    controls: "Đánh hoặc nhấn nút thích hợp cho « sửa » hay « Không đúng ».",
    walkthrough: [
      "Một từ nhấp nháy trên màn hình.",
      "Nhanh chóng phân tích chính tả.",
      "Quyết định nếu nó là chính tả hợp lệ hoặc chứa lỗi đánh dấu.",
      "Hãy quyết định trước khi hết giờ.",
    ],
    strategies: [
      "Tin tưởng nhận diện trực quan ngay lập tức của bạn; chính xác đánh vần từ thường \"nhìn\" bên phải.",
      "Coi chừng những cặp tinh xảo thông thường như 'ie' v 'ei' và hai phần phụ âm.",
      "Đừng suy nghĩ quá nhiều, vì thời gian giới hạn rất nghiêm ngặt.",
    ],
  ),
  "spoonerism_solver": (
    objective: "Thay đổi âm thanh ban đầu của hai từ để giải đáp các đầu mối.",
    controls: "Gõ hoặc chọn những từ đúng được tạo ra bởi ma- li.",
    walkthrough: [
      "Đọc manh mối được cung cấp trên màn hình.",
      "Câu trả lời là một cặp từ có nghĩa là một câu nói thông thường khác.",
      "Xác định cụm từ đích và trao đổi chữ cái đầu tiên/ âm thanh.",
      "Hãy nhập hai từ để giải câu đố.",
    ],
    strategies: [
      "Âm thanh lớn tiếng, giống như người theo phái yêu tinh dựa trên âm thanh, không chỉ đánh vần.",
      "Hãy tìm những thành ngữ phổ biến hoặc những cặp nổi tiếng như là cụm từ cơ bản.",
      "Hãy tìm ngược từ manh mối để tìm ra những từ đã thay đổi.",
    ],
  ),
  "spotlight_track": (
    objective: "Theo dõi nhiều mục tiêu di chuyển trong bóng tối khi chúng được chiếu sáng ngắn gọn.",
    controls: "Tấn công vị trí của mục tiêu sau khi chúng ngừng di chuyển.",
    walkthrough: [
      "Các mục tiêu được tô sáng ngay từ đầu.",
      "đèn tắt, và mọi đồ vật bắt đầu di chuyển.",
      "Sự chú ý cho thấy sơ qua vị trí của họ khi họ di chuyển.",
      "Khi chúng dừng lại, hãy vỗ vào tất cả các mục tiêu ban đầu.",
    ],
    strategies: [
      "Đừng tập trung vào một mục tiêu duy nhất; hãy giữ một cái nhìn rộng và thoải mái.",
      "Sử dụng ánh đèn chiếu sáng để cập nhật bản đồ tinh thần của các mục tiêu.",
      "Dự đoán nơi họ sẽ dựa trên tốc độ và hướng đi của họ.",
    ],
  ),
  "staircase_memory": (
    objective: "Ghi nhớ chuỗi các biểu tượng đã tô sáng trên một lưới, sau đó chọn chính xác những biểu tượng từ một mạng lưới các tùy chọn để có thể tái tạo lại thiết lập.",
    controls: "Gõ vào các biểu tượng ở lưới dưới được hiển thị trong chuỗi trên cùng.",
    walkthrough: [
      "Xem chuỗi các ảnh tượng được tô sáng.",
      "Xem hệ thống tùy chọn biểu tượng được cung cấp.",
      "Gõ tất cả các biểu tượng từng là một phần của chuỗi được tô sáng.",
      "Chọn thành công tất cả các biểu tượng đúng để tiến tới một chuỗi dài hơn.",
    ],
    strategies: [
      "Các biểu tượng nhóm theo màu hoặc phân loại để nhớ chúng dễ dàng hơn.",
      "Hãy tạo ra một câu chuyện ngắn trong đầu bạn bằng cách sử dụng các biểu tượng khi chúng xuất hiện.",
    ],
  ),
  "sternberg_task": (
    objective: "Ghi nhớ một chuỗi ngắn các chữ cái được hiển thị một thời gian ngắn, sau đó xác định nếu một chữ cái thăm dò duy nhất xuất hiện trong chuỗi đó.",
    controls: "Nhấn nút CÓ nếu lá thư thăm dò có trong chuỗi, hoặc nút NO nếu không.",
    walkthrough: [
      "Ghi nhớ tập hợp các chữ cái được hiển thị trên màn hình.",
      "Chờ cho chuỗi biến mất và chỉ xuất hiện một chữ cái thăm dò.",
      "Hãy nhớ nếu lá thư thăm dò là một phần của bộ gốc.",
      "Tap Yes hoặc NO trước khi thời gian hết.",
    ],
    strategies: [
      "Nói lớn tiếng hoặc thầm lặng trong đầu bạn khi chúng xuất hiện.",
      "Nhóm các chữ cái lại thành mảng hoặc âm tiết có khả năng phát âm nếu có thể.",
    ],
  ),
  "stop_signal": (
    objective: "Nhanh chóng nhấn nút mũi tên phù hợp với hướng của mũi tên màu xanh lá cây lớn, trừ phi mũi tên chuyển sang màu đỏ, trong trường hợp bạn không phải làm gì và chờ đợi.",
    controls: "Ấn nút mũi tên trái nếu mũi tên màu xanh lá cây chỉ trái, hoặc cái nút mũi tên phải nếu nó chỉ đúng. Đừng gõ bất cứ cái gì nếu mũi tên màu đỏ.",
    walkthrough: [
      "Chờ mũi tên xanh lá cây lớn xuất hiện trên màn hình.",
      "Nhanh chóng nhấn nút trái hoặc phải tương ứng.",
      "Nếu mũi tên đột nhiên chuyển sang màu đỏ (dấu hiệu dừng lại), hãy ngừng gõ và đợi thử nghiệm tiếp theo.",
      "Duy trì độ chính xác cao và tốc độ vượt qua nhiều thử thách.",
    ],
    strategies: [
      "Giữ ngón cái của bạn lơ lửng gần nút để giảm thiểu thời gian phản ứng.",
      "Đừng dự đoán hướng đi; đợi tín hiệu thị giác trước khi di chuyển.",
    ],
  ),
  "story_builder": (
    objective: "Xây dựng lại một câu chuyện bằng cách chọn các câu theo thứ tự thời gian chính xác.",
    controls: "Hãy gõ các lá bài câu theo thứ tự họ nên xuất hiện để xây dựng câu chuyện.",
    walkthrough: [
      "Hãy đọc cẩn thận tất cả các đoạn văn được rải rác.",
      "Xác định câu bắt đầu câu chuyện một cách hợp lý và gõ nó.",
      "Tìm câu logic tiếp theo sau đó và gõ nó.",
      "Tiếp tục chọn câu cho đến khi câu chuyện hoàn toàn được dựng lại.",
    ],
    strategies: [
      "Tìm kiếm các từ chuyển tiếp như \"đầu tiên\", sau đó \"sau đó\", hoặc \"sau cùng\" để suy ra trật tự.",
      "Xác định mối quan hệ gây ra và hiệu quả giữa các câu.",
    ],
  ),
  "stroop_test": (
    objective: "Hãy xác định màu của văn bản đã hiển thị, bỏ qua từ đã ghi (có thể đánh dấu màu mâu thuẫn).",
    controls: "Ấn nút chứa tên của màu mực, bỏ qua từ đó.",
    walkthrough: [
      "Xem từ đã hiển thị ở giữa màn hình.",
      "Bỏ qua những gì từ này nói, và nhận ra màu mực thật sự được vẽ trong đó.",
      "Tìm cái nút có màu mực.",
      "Nhấn nút đúng càng nhanh càng tốt trước khi hết giờ.",
    ],
    strategies: [
      "Hãy thử liếc mắt một chút để che mờ từ và chỉ tập trung vào màu sắc.",
      "Hãy nhắc lại màu mà bạn thấy trước khi xem xét các lựa chọn.",
    ],
  ),
  "sudoku": (
    objective: "Điền vào lưới 9x9 để cho mỗi hàng, cột, và 3x3 hộp chứa các chữ số 1 đến 9 chính xác một lần mà không có bản sao nào.",
    controls: "Hãy gõ một ô rỗng trên lưới để chọn nó, rồi gõ một số từ bàn phím dưới để điền vào nó. Hãy gõ lại ô đã chọn, hoặc nút rõ để xoá một số.",
    walkthrough: [
      "Quét lưới để tìm hàng, cột, hoặc 3x3 hộp gần đầy.",
      "Mở một buồng giam trống ở một trong những khu vực đó.",
      "Xác định số còn thiếu và chọn nó từ bàn phím.",
      "Lặp lại quá trình này, sử dụng logic để suy ra những con số mất tích cho đến khi toàn bộ mạng lưới được điền đúng.",
    ],
    strategies: [
      "Bắt đầu với 3x3 hộp có nhiều số nhất cho trước.",
      "Tìm những người độc thân khỏa thân mà chỉ có một số cụ thể có thể vừa với một tế bào dựa trên hàng, cột và hộp.",
    ],
  ),
  "sum_pyramid": (
    objective: "Điền vào những khối trống của kim tự tháp để số của mỗi khối là số chính xác của hai khối ngay bên dưới nó.",
    controls: "Hãy gõ vào một khối trống trong kim tự tháp để chọn nó, rồi dùng bảng số để nhập giá trị đúng. Hãy gõ vào nút Không gian lùi để xóa lỗi.",
    walkthrough: [
      "Tìm một khối trống có cả hai khối bên dưới, hoặc một khối đã lấp đầy với một khối bên dưới.",
      "Gõ vào khối trống để chọn nó.",
      "Tính tổng hay hiệu số rồi nhập số bằng bàn phím.",
      "Hãy đưa ra câu trả lời để kiểm tra xem kim tự tháp có được giải quyết đúng không.",
    ],
    strategies: [
      "Làm việc từ dưới lên khi bạn có các số cơ sở lân cận.",
      "Làm việc từ trên xuống dưới sử dụng trừ khi bạn có một khối trên cùng và một trong những khối nền tảng của nó.",
    ],
  ),
  "sum_snake": (
    objective: "Theo dõi một đường dẫn liên tục, không quá tải thông qua các mạng lưới các con số để tổng số của các con số trên đường đi chính xác bằng giá trị đích.",
    controls: "Gõ và kéo qua các tế bào lưới bên cạnh (thường, theo chiều dọc, hoặc dọc) để vẽ đường dẫn của bạn.",
    walkthrough: [
      "Ghi chú tổng mục tiêu cần thiết ở đầu màn hình.",
      "Tìm số khởi động trên mạng đi.",
      "Kéo ngón tay qua số kề, theo dõi số đang chạy.",
      "Thả ngón tay ra khi tổng của con đường đã tô sáng trùng với đích chính xác.",
    ],
    strategies: [
      "Nếu mục tiêu lớn, hãy tìm đường có số lượng cao.",
      "Nếu bạn bắn quá mục tiêu, hãy truy ngược lại đường đi của bạn để khử các tế bào.",
    ],
  ),
  "switch_task": (
    objective: "Khớp biểu tượng trung tâm với một trong những tùy chọn dựa trên quy tắc hoạt động hiện thời (hoặc tương ứng với COLOR hoặc khớp với HPE), mà thay đổi năng động.",
    controls: "Nhấn vào nút tùy chọn (trái hay phải) khớp với biểu tượng trung tâm theo quy tắc hiện có ở trên cùng.",
    walkthrough: [
      "Đọc các quy tắc hiện tại ở đầu màn hình (MASPOR hoặc MLPE phù hợp).",
      "Quan sát biểu tượng trung tâm và đặc tính của nó.",
      "Hãy so sánh với hai lựa chọn được cung cấp.",
      "Gõ tùy chọn khớp với quy tắc hoạt động trước khi hết thời gian.",
    ],
    strategies: [
      "Luôn luôn đọc quy tắc trước khi nhìn vào các biểu tượng, vì nó thay đổi thường xuyên.",
      "Verbally lặp lại quy tắc để giữ tập trung.",
    ],
  ),
  "syllable_stack": (
    objective: "Kết hợp các âm tiết rải rác theo thứ tự đúng để tạo thành những từ hoàn chỉnh và hợp lệ.",
    controls: "Gõ vào các khối âm tiết trong chuỗi đúng để tạo ra một từ. Hãy nhắp vào nút hoàn nguyên để gỡ bỏ âm tiết đã chọn cuối cùng.",
    walkthrough: [
      "Xem các âm tiết có sẵn rải rác trên màn hình.",
      "Hãy cố gắng nhận ra từ quen thuộc bắt đầu hoặc kết thúc.",
      "Gõ âm tiết để xây dựng một từ trong khe hoạt động.",
      "Một khi đã tạo một từ hợp lệ, nó sẽ khóa lại; tiếp tục cho đến khi mọi âm tiết được dùng.",
    ],
    strategies: [
      "Tìm kiếm các tiền tố chung (như 're-' hoặc 'un-') hoặc hậu tố (như '-tion' hay '-ing').",
      "Âm thanh cho thấy sự kết hợp trong đầu bạn trước khi chọn chúng.",
    ],
  ),
  "symbol_digit_assoc": (
    objective: "Ghi nhớ sự kết hợp giữa 9 ký hiệu độc đáo và các chữ số 1-9, sau đó dịch chính xác một chuỗi các ký hiệu thách thức vào các chữ số tương ứng bằng bàn phím.",
    controls: "Trong giai đoạn nhớ lại, gõ một hộp biểu tượng để chọn nó, rồi gõ vào mục số để nhập vào con số tương ứng. Hãy nhắp vào cái nút rõ ràng để xoá mục nhập, rồi nộp khi hoàn tất.",
    walkthrough: [
      "Hãy nghiên cứu chìa khóa liên kết cho thấy biểu tượng nào bằng số nào.",
      "Bắt đầu chạy bàn phím để giấu chìa khóa và bắt đầu kiểm tra.",
      "Hãy xem những biểu tượng thử thách được cung cấp.",
      "Dùng bàn phím để nhập số đúng cho mỗi biểu tượng từ bộ nhớ và phục tùng.",
    ],
    strategies: [
      "Tạo ra những câu chuyện trực quan liên kết hình dạng của biểu tượng với con số.",
      "Tập trung vào việc ghi nhớ 3 hay 4 cặp cùng một lúc thay vì tất cả 9 cặp cùng một lúc.",
    ],
  ),
  "symbolic_flanker": (
    objective: "Xác định biểu tượng trung tâm trong một hàng năm ký hiệu, bỏ qua các biểu tượng cạnh hông ở hai bên, mà có thể giống nhau hoặc khác nhau.",
    controls: "Ấn nút tương ứng với biểu tượng trung tâm.",
    walkthrough: [
      "Hàng năm ký hiệu sẽ xuất hiện trên màn hình.",
      "Hoàn toàn tập trung vào biểu tượng trung tâm, lờ đi hai bên trái và hai bên phải.",
      "Xác định biểu tượng trung tâm.",
      "Nhanh chóng nhấn nút biểu tượng khớp ở dưới màn hình.",
    ],
    strategies: [
      "Hãy cố gắng sửa cái nhìn của bạn vào trung tâm chính xác của màn hình trước khi các biểu tượng xuất hiện.",
      "Ý thức buộc bản thân phải bỏ qua các cạnh bên ngoài của dòng biểu tượng.",
    ],
  ),
  "symbol_logic": (
    objective: "Deduce giá trị số của các ký hiệu khác nhau dựa trên một loạt các phương trình thị giác, sau đó tính toán và nhập câu trả lời cho câu hỏi cuối cùng.",
    controls: "Dùng bảng số để gõ câu trả lời cho phương trình cuối cùng. Hãy nhắp vào cái nút rõ ràng cần xoá, và cái nút đánh dấu cần gởi lời đoán.",
    walkthrough: [
      "Xem xét phương trình đầu tiên để xác định giá trị của biểu tượng đầu tiên (v. g., A + A = X).",
      "Dùng giá trị đó trong phương trình tiếp theo để giải cho biểu tượng thứ hai.",
      "Tiếp tục thay thế các giá trị đã biết để tìm giá trị của mọi biểu tượng.",
      "Tính tổng của các biểu tượng trong phương trình cuối cùng và nhập câu trả lời.",
    ],
    strategies: [
      "Luôn luôn bắt đầu với phương trình có hai biểu tượng giống hệt nhau.",
      "Ghi lại giá trị của các biểu tượng nếu bạn thấy khó giữ chúng trong trí nhớ.",
    ],
  ),
  "symmetry": (
    objective: "Hoàn thành mô hình đối xứng bằng cách đảo lộn các tế bào ở nửa phải của lưới để nó phản chiếu hoàn hảo nửa trái trước khi đầy.",
    controls: "Gõ hoặc kéo qua các ô rỗng bên phải của lưới để bật hoặc tắt chúng để phù hợp với sự phản chiếu.",
    walkthrough: [
      "Quan sát mẫu tế bào được lấp đầy bên trái của lưới.",
      "Hãy hình dung một đường gương thẳng đứng ở giữa lưới điện.",
      "Gõ các tế bào bên phải để đặt chúng vào vị trí được soi gương.",
      "Bảo vệ phía bên phải là phản ánh chính xác phía bên trái để hoàn thành câu đố.",
    ],
    strategies: [
      "Cột làm việc bằng cột, bắt đầu từ giữa đường gương và di chuyển ra ngoài.",
      "Đếm các khoảng trống từ dòng giữa đến vị trí chính xác vị trí các tế bào được soi gương.",
    ],
  ),
  "symmetry_span": (
    objective: "Thay đổi giữa việc đánh giá các mẫu có cân xứng hay không và ghi nhớ vị trí của hồng cầu trong một mạng lưới 4x4, rồi nhớ lại toàn bộ chuỗi các vị trí hồng cầu theo thứ tự.",
    controls: "Khi nhớ lại, hãy gõ vào lưới 4x4 theo thứ tự chính xác của hồng cầu.",
    walkthrough: [
      "Ghi nhớ vị trí của tế bào đỏ trên mạng lưới.",
      "Xem xét ma trận kế tiếp có cân xứng với việc gõ có hay không.",
      "Ghi nhớ vị trí hồng cầu tiếp theo.",
      "Một khi giai đoạn thu hồi bắt đầu, hãy gõ các tế bào lưới theo trình tự chính xác của hồng cầu.",
    ],
    strategies: [
      "Hãy thử hình dung một đường nối các hồng cầu với nhau để nhớ trình tự của chúng.",
      "Tập trung vào độ chính xác trong suốt quá trình đánh giá đối xứng, nhưng đừng để nó làm cậu sao lãng việc lặp lại chuỗi suy nghĩ trong đầu.",
    ],
  ),
  "tangle_fix": (
    objective: "Gỡ rối đồ thị bằng cách di chuyển các nút để không có các đường nối kết nối nhau.",
    controls: "Gõ và giữ một nút, sau đó kéo nó xung quanh màn hình để định vị và tách các đường kết nối.",
    walkthrough: [
      "nhìn vào mạng lưới các nút rối loạn và các đường cắt nhau.",
      "Xác định những đường đang đi qua (có màu đỏ cao).",
      "Kéo các nút nối với các đường đó đến các vị trí mới.",
      "Tiếp tục định vị các nút cho đến khi mọi đường đều rõ ràng và không còn giao nhau (trở lại xanh lá cây).",
    ],
    strategies: [
      "Cố gắng kéo nút có nhiều kết nối tới trung tâm, và nút có kết nối với bên ngoài.",
      "Tìm những hình tam giác hoặc vòng lặp của các nút nối và tháo chúng ra như một nhóm.",
    ],
  ),
  "tangram": (
    objective: "Hãy điền đầy đủ các đường nét mục tiêu vào lưới bằng cách đặt và xoay tất cả các mảnh tangram đã cung cấp mà không cần chồng lên nhau.",
    controls: "Đập một mảnh ở bến tàu để chọn nó, hai mặt để xoay nó, và gõ một tế bào vào lưới để đặt điểm xoay của mảnh đó.",
    walkthrough: [
      "Quan sát hình vẽ mục tiêu trên lưới chính.",
      "Gõ một miếng ở bến tàu để chọn nó.",
      "Gấp đôi phần nếu bạn cần xoay nó để phù hợp.",
      "Nhấn vào lưới để đặt mảnh, và lặp lại cho đến khi hình dạng mục tiêu được lấp đầy hoàn hảo.",
    ],
    strategies: [
      "Bắt đầu bằng cách đặt những mảnh lớn nhất hoặc những mảnh có hình dạng độc đáo chỉ vừa với những góc cụ thể.",
      "Nếu bạn bị mắc kẹt, hãy gỡ bỏ các mảnh và thử một vòng quay khác cho mảnh đầu tiên.",
    ],
  ),
  "target_10": (
    objective: "Chọn một tổ hợp các miếng gạch số từ lưới 5x5 có tổng bằng 10.",
    controls: "Hãy gõ các miếng trên lưới để chọn hay hủy bỏ chúng và thêm các giá trị của chúng vào tổng số lựa chọn hiện thời.",
    walkthrough: [
      "nhìn vào các con số sẵn có trên mạng lưới 5x5.",
      "Gõ số điện thoại để bắt đầu sự lựa chọn.",
      "Gõ số bổ sung, để ý chỉ thị tổng kết.",
      "Chọn một tổ hợp chính xác là 10 để làm sạch những điểm và điểm.",
    ],
    strategies: [
      "Tìm kiếm các cặp rõ ràng làm cho 10, như 9 + 1 hoặc 8 + 2.",
      "Bạn có thể sử dụng ba hay nhiều số (ví dụ, 5 + 3+2) nếu không có các cặp đơn giản.",
    ],
  ),
  "target_number": (
    objective: "Sử dụng các số lượng cung cấp và toán học tổng hợp để xây dựng một biểu thức mà đánh giá chính xác đến số mục tiêu.",
    controls: "Hãy gõ các miếng gạch số và các nút điều khiển để tạo ra biểu thức của bạn. Hãy nhắp vào cái nút xóa để gỡ bỏ thông tin nhập cuối cùng, hoặc làm tươi để làm sạch hoàn toàn.",
    walkthrough: [
      "Ghi chú số mục tiêu ở đầu màn hình.",
      "Xem các miếng số có sẵn.",
      "Những con số và những nhà điều hành để xây dựng một phương trình toán học.",
      "Dùng tất cả các con số để đạt được giá trị đích xác để thắng vòng.",
    ],
    strategies: [
      "Hãy nghĩ ngược lại từ số mục tiêu để xem nếu một phép nhân hoặc bước chia có thể đưa bạn đến gần.",
      "Dùng dấu ngoặc để kiểm soát thứ tự hoạt động khi thêm hay trừ trước khi nhân.",
    ],
  ),
  "temporal_order": (
    objective: "Ghi nhớ một chuỗi các biểu tượng được trình bày từng cái một, rồi trả lời các câu hỏi về những biểu tượng được cho trước hoặc sau này xuất hiện trong chuỗi.",
    controls: "Ấn nút tương ứng với biểu tượng trả lời các yêu cầu.",
    walkthrough: [
      "Mỗi lần một người được xem một loạt ảnh tượng.",
      "Đọc câu hỏi để biết bạn cần xác định dấu vết hay vật sau đó.",
      "Xem hai tùy chọn biểu tượng được cung cấp.",
      "Nhấn vào biểu tượng phù hợp với yêu cầu thời gian.",
    ],
    strategies: [
      "Tạo ra một câu chuyện liên kết các biểu tượng với nhau theo thứ tự chúng có vẻ như để củng cố chuỗi ký ức của bạn.",
      "Hãy đọc thuộc lòng danh sách các mục mỗi lần thêm một mục mới.",
    ],
  ),
  "tenner_grid": (
    objective: "Điền vào lưới để mỗi hàng chứa các chữ số 0-9 một lần, tổng số của mỗi cột khớp với số mục tiêu bên dưới nó, và không có tế bào bên cạnh (ngay cả chéo) chứa cùng một số.",
    controls: "Gõ vào một ô trống trên lưới để chọn nó, rồi gõ một số từ bàn phím bên dưới để điền vào.",
    walkthrough: [
      "Mở một buồng giam trống trong lưới.",
      "Xem mục tiêu cột tổng và các số khác trong cột đó.",
      "Chọn một số từ bàn phím để giúp đạt được tổng mà không cần phải phức tạp hóa một số nào đó trong hàng, hoặc đặt nó cạnh một số giống hệt.",
      "Lấp đầy toàn bộ lưới theo mọi luật lệ để chiến thắng.",
    ],
    strategies: [
      "Bắt đầu với các cột có tổng mục tiêu cao hoặc thấp, vì chúng có ít tổ hợp có thể.",
      "Hãy chú ý đến quy tắc mà cùng một số không thể chạm chéo.",
    ],
  ),
  "tents_and_trees": (
    objective: "Đặt những căn lều trong lưới để mỗi cây được kết hợp chính xác với một cái lều gần nhau, không có hai cái lều nào đụng nhau (ngay cả hai chéo), và đền tạm được tính theo hàng và cột.",
    controls: "Hãy đập một tế bào trống để đặt một cái lều, vỗ một lần nữa để đạp lên cỏ (không có gì) hoặc vỗ lần nữa để rõ ràng.",
    walkthrough: [
      "Hãy nhìn vào hàng và cột manh mối cho thấy mỗi hàng có bao nhiêu cái lều.",
      "Tìm cây cối và vòi gần các phòng trống để đặt lều bên cạnh.",
      "Bảo đảm không có hai cái lều nào chạm vào nhau, thậm chí chéo nhau.",
      "Hoàn tất lưới điện để tất cả cây đều có lều và mọi manh mối đều được thỏa mãn.",
    ],
    strategies: [
      "Điền đầy hàng hoặc cột với một đầu mối '0' hoàn toàn bằng cỏ.",
      "Nếu một cái cây chỉ có một khoảng trống hợp lệ bên cạnh nó, thì một cái lều phải được đặt ở đó.",
    ],
  ),
  "topology": (
    objective: "Xác định nếu hai ký tự hoặc hình dạng được trưng bày tương đương nhau về mặt tâm lý, có nghĩa là một có thể bị kéo giãn hoặc biến dạng thành cái khác mà không làm rách hoặc trộn lỗ.",
    controls: "Nếu không có nút NO, hãy nhấn vào nút Yes nếu chúng có tính chất siêu đẳng.",
    walkthrough: [
      "Hãy nhìn hai hình hoặc ký tự được trình bày trên màn hình.",
      "Đếm số lỗ trong mỗi hình.",
      "Xem xét số điểm cuối hoặc giao điểm.",
      "Vâng, nếu họ có cùng đặc tính địa chất, hoặc không, nếu họ khác nhau.",
    ],
    strategies: [
      "Đặc điểm quan trọng nhất là số lượng các lỗ; một 'O' và 'D' tương đương với (1 lỗ), nhưng một 'O' và một '8' không phải là (1 với 2 lỗ).",
      "Hãy tưởng tượng hình dạng của nó được làm bằng cao su và xem bạn có thể uốn cong cái này vào cái kia không.",
    ],
  ),
  "tower_of_london": (
    objective: "Di chuyển các hạt màu giữa ba cái chốt để phù hợp với cấu hình mục tiêu trong số lượng di chuyển tối thiểu, bám chặt vào khả năng cao của mỗi cái chốt.",
    controls: "Gõ một cái chốt để chọn hạt ở trên, sau đó gõ một cái chốt khác để di chuyển hạt ở đó.",
    walkthrough: [
      "So sánh bố trí của chuỗi hạt hiện thời ở các chốt dưới cùng với cấu hình đích trên cùng.",
      "Gõ cái cần câu mà anh muốn di chuyển.",
      "Gõ cái chốt điểm đến để thả hạt, nhớ rằng các chốt chỉ có thể giữ 3, 2, và 1 chuỗi hạt.",
      "Khớp cấu hình đích trước khi không còn khả năng di chuyển.",
    ],
    strategies: [
      "Lên kế hoạch di chuyển ngược từ cấu hình đích để tìm ra hạt nào cần được đặt trước.",
      "Dùng cái móc nhỏ nhất (thành phố 1) làm chỗ tạm thời để truy cập hạt bên dưới.",
    ],
  ),
  "trace_path": (
    objective: "Hãy cẩn thận lần theo con đường đã được vẽ từ điểm đầu đến điểm cuối, càng sát với dòng chữ càng tốt để đạt được độ chính xác cao.",
    controls: "Gõ và giữ điểm khởi động, sau đó kéo ngón tay của bạn dọc theo con đường đến điểm kết thúc.",
    walkthrough: [
      "Xác định điểm bắt đầu của đường mục tiêu.",
      "Nhấn và giữ ngón tay ở điểm khởi động.",
      "Kéo ngón tay trên đường cong, cố gắng đứng chính xác trên đường kẻ.",
      "Hãy thả ngón tay ra khi bạn đạt đến dấu chấm hết để đạt điểm chính xác.",
    ],
    strategies: [
      "Di chuyển với tốc độ ổn định, ôn hòa; di chuyển quá nhanh giảm đi độ chính xác, nhưng di chuyển quá chậm khiến việc vẽ đường cong mịn trở nên khó.",
      "Hãy nhìn trước một chút để biết trước những đường cong.",
    ],
  ),
  "trail_making": (
    objective: "Kết nối các vòng tròn có số hoặc chữ cái theo thứ tự chính xác càng nhanh càng tốt.",
    controls: "Đánh các vòng tròn theo đúng trình tự.",
    walkthrough: [
      "Tìm vòng tròn đầu tiên trong chuỗi và gõ nó.",
      "Nhanh chóng quét màn hình cho mục hợp lý tiếp theo trong chuỗi.",
      "Gõ vòng tiếp theo để kết nối chúng.",
      "Tiếp tục nối các vòng tròn theo thứ tự đúng cho đến khi con đường mòn hoàn tất.",
    ],
    strategies: [
      "Trong khi di chuyển ngón tay của bạn đến vòng tròn tiếp theo, tích cực quét phần còn lại của màn hình cho một vòng sau đó.",
      "Giữ ngón tay của bạn gần màn hình để giảm thiểu thời gian du lịch.",
    ],
  ),
  "triplets_logic": (
    objective: "Điền một lưới 6x6 với ba loại hình để cho mỗi hàng và cột có chính xác hai hình dạng, và không có ba hình giống hệt nhau xuất hiện liên tục trong bất kỳ hàng hoặc cột nào.",
    controls: "Hãy gõ vào một công cụ hình dạng để chọn nó, rồi gõ vào một tế bào trống trên lưới để sơn hình đó.",
    walkthrough: [
      "Chọn một hình từ trình đơn công cụ bên dưới lưới.",
      "Mở một ô trống để đặt hình đã chọn.",
      "Dùng logic để đảm bảo không có ba hình giống hệt nhau kề theo chiều dọc hoặc chiều ngang.",
      "Làm cho chắc mỗi hàng và cột chứa đúng hai hình dạng để hoàn tất câu đố.",
    ],
    strategies: [
      "Nếu bạn thấy hai hình dạng giống hệt nhau bên cạnh nhau, khoảng trống ở hai bên phải là các hình dạng khác nhau.",
      "Nếu một hàng đã có hai hình dạng nhất định, hãy điền vào các ô rỗng còn lại với các hình khác.",
    ],
  ),
  "typing_speed": (
    objective: "Hãy gõ chính xác cụm từ được hiển thị càng nhanh càng tốt để thử từ trong mỗi phút (WPM).",
    controls: "Dùng bàn phím trên màn hình để gõ đoạn văn đích vào trường văn bản.",
    walkthrough: [
      "Đọc cụm từ đích được hiển thị ở giữa màn hình.",
      "Gõ vào ô nhập văn bản để thêm bàn phím.",
      "Gõ chính xác cụm từ này, chú ý đến các ký tự khớp.",
      "Hoàn thành câu trước khi đồng hồ hẹn giờ hết hạn để xem điểm WPM của bạn.",
    ],
    strategies: [
      "Tập trung vào độ chính xác đầu tiên; sửa chữa lỗi thì mất nhiều thời gian hơn là gõ chậm hơn một chút nhưng đúng.",
      "Hãy cố gắng đọc trước vài từ bạn đang gõ.",
    ],
  ),
  "typoglycemia_decoder": (
    objective: "Hãy giải thích và đọc những chữ trong đó được trộn lẫn, chỉ giữ những chữ đầu tiên và cuối cùng đúng.",
    controls: "Gõ chính xác từ không xáo trộn hoặc chọn nó từ nhiều lựa chọn.",
    walkthrough: [
      "Một từ được hiển thị với các chữ trong bộ trộn (ví dụ 'Tpyolgcyre').",
      "Hãy nhìn những chữ cái đầu tiên và cuối cùng để nắm bắt từ bộ xương.",
      "Giải mã cấu trúc gốc của từ.",
      "Gõ hoặc chọn từ đúng cần tiếp tục.",
    ],
    strategies: [
      "Hãy đọc từ này với tư cách là một thực thể riêng lẻ thay vì phân tích vị trí chữ cái riêng lẻ.",
      "Tập trung vào ngữ cảnh nếu từ này là một phần của câu văn đầy đủ.",
      "Não của bạn tự nhiên nhận ra từ ngữ nếu giới hạn bên ngoài được đặt đúng chỗ.",
    ],
  ),
  "unit_converter_pro": (
    objective: "Chuyển đổi giá trị giữa các đơn vị đo lường khác nhau (ví dụ độ C sang nhiệt độ, mét sang feet).",
    controls: "Hãy nhập vào tên giá trị đã sửa đổi trên bảng số và đệ lại.",
    walkthrough: [
      "Lưu ý giá trị bắt đầu, đơn vị và đơn vị đo lường của mục tiêu.",
      "Tính giá trị cải đạo bằng cách nhân số hay công thức thích hợp.",
      "Nhập giá trị đích tính trên numpad.",
      "Hãy chấp nhận để xác minh câu trả lời của bạn.",
    ],
    strategies: [
      "Hãy ghi nhớ những điểm chuẩn cơ bản trong quá trình chuyển đổi (ví dụ 1 inch = 2.54 cm, 0°C = 32 °F).",
      "Tính toán nếu giá trị chính xác là phức tạp.",
      "Chú ý đến các đơn vị để tránh các hợp đồng hoán đổi nhân của Division.",
    ],
  ),
  "vector_grid_alignment": (
    objective: "Sắp xếp véc- tơ trên lưới để chỉ theo cùng một hướng hoặc tạo một trường dòng đặc trưng.",
    controls: "Gõ hoặc kéo véc tơ quay và thay đổi hướng của chúng.",
    walkthrough: [
      "Theo dõi hướng hoặc kiểu mẫu cần thiết.",
      "Chọn các véc- tơ cá nhân bị lỗi.",
      "Xoay chúng cho đến khi chúng khớp với dòng hướng mục tiêu.",
      "Sửa đổi mọi véc- tơ để hoàn thành câu đố.",
    ],
    strategies: [
      "Bắt đầu bằng cách canh lề véc- tơ cạnh các đường biên.",
      "Tìm nhóm quay nếu có thể.",
      "Kiểm tra toàn bộ lĩnh vực lưu thông để bắt những sai sót nhỏ.",
    ],
  ),
  "vektor_vector": (
    objective: "Thực hiện thao tác véc- tơ (dùng, trừ, phóng to) trên mặt phẳng tọa độ.",
    controls: "Kéo mũi tên véc- tơ kết thúc để khớp với kết quả tính toán véc- tơ.",
    walkthrough: [
      "Lưu ý phương trình véc tơ toán học (ví dụ A + B hay 2A).",
      "Thêm hoặc nhân thành phần của véc- tơ khởi động.",
      "Kéo kết quả đầu véc- tơ tới tọa độ đúng.",
      "Đề nghị xác nhận sự thẳng hàng.",
    ],
    strategies: [
      "Tính từng thành phần (phần X trước, sau là Y).",
      "Để thêm véc tơ, hãy tưởng tượng xếp mũi tên đầu vào đuôi.",
      "Kiểm tra 2 lần tọa độ thành phần âm tính cẩn thận.",
    ],
  ),
  "venn_numbers": (
    objective: "Đặt con số vào những giao điểm chính xác của biểu đồ Venn theo tính chất số.",
    controls: "Kéo và thả các biểu tượng số vào phần sơ đồ Venn.",
    walkthrough: [
      "Đọc thẻ thuộc tính cho mỗi vòng tròn (ví dụ 'Prime', 'Cuest', 'Maltiple of 3').",
      "Phân tích tính chất của biểu tượng số cho trước.",
      "Kéo số vào giao lộ, nơi nó thỏa mãn mọi tính chất vòng tròn khớp.",
      "Đặt tất cả các con số chính xác để giành chiến thắng.",
    ],
    strategies: [
      "Kiểm tra nếu số này không khớp với phân loại nào và thuộc về ranh giới bên ngoài.",
      "Hãy dành thời gian để xác định mức độ chồng chéo của vòng tròn.",
      "Tìm những con số phù hợp với giao lộ trung tâm của tất cả các vòng tròn đầu tiên.",
    ],
  ),
  "verbal_analogies": (
    objective: "Hoàn thành phép so sánh mối quan hệ (ví dụ nóng là lạnh như lên...).",
    controls: "Hãy gõ chính xác từ để hoàn thành phép so sánh.",
    walkthrough: [
      "Đọc mối quan hệ tương tự bắt đầu (A là B).",
      "Xác định logic của mối quan hệ (ví dụ đối lập, đồng nghĩa, công cụ/người dùng).",
      "áp dụng cùng một logic cho từ đích (C là...).",
      "Gõ từ ngữ phù hợp với logic này.",
    ],
    strategies: [
      "Xác định mối quan hệ chính xác giữa hai từ đầu trong một câu đơn giản.",
      "Bảo đảm các từ khớp (ví dụ A là hành động và B là danh từ, C phải hành động và D phải là danh từ).",
      "Loại bỏ các tùy chọn thuộc về nhóm từ không liên quan.",
    ],
  ),
  "vigilance_task": (
    objective: "Giữ sự chú ý trong một thời gian dài và chỉ phản ứng trước những tín hiệu hiếm khi xảy ra trong khi lờ đi những người hay bị phân tâm.",
    controls: "Chỉ gõ vào màn hình khi có tín hiệu mục tiêu hiếm.",
    walkthrough: [
      "Quan sát tín hiệu phân tâm thường xuyên nhấp nháy.",
      "Giữ tập trung và lờ đi những biến thể gây phân tâm.",
      "Phản ứng ngay khi có tín hiệu mục tiêu đặc biệt hiếm có.",
      "Tiếp tục giám sát trong thời gian thi hành nhiệm vụ.",
    ],
    strategies: [
      "Giữ nhịp thở đều đặn để tránh mệt mỏi.",
      "Không chạm vào mỗi chớp; đợi để xác nhận hình dạng/ màu của mục tiêu.",
      "Giữ tập trung vào khu vực kích thích.",
    ],
  ),
  "visual_search": (
    objective: "Tìm biểu tượng mục tiêu độc nhất vô nhị trong số những người đánh lạc hướng như vậy.",
    controls: "Đánh vào biểu tượng mục tiêu trong mạng lưới.",
    walkthrough: [
      "Đọc mô tả mục tiêu hoặc bố trí biểu tượng cần tìm.",
      "Quét nhanh các thiết bị đánh lạc hướng.",
      "Xác định mục đích duy nhất.",
      "Nhấn nút để ghi điểm và tiến lên.",
    ],
    strategies: [
      "Quét trong một đường dẫn lưới hệ thống (ví dụ hàng trái sang phải) thay vì tìm kiếm ngẫu nhiên.",
      "Hãy tìm những tính năng nổi bật (chẳng hạn như hướng hoặc màu).",
      "Nếu mục tiêu có tính năng riêng biệt, hãy tìm sự khác biệt đó.",
    ],
  ),
  "visual_statistical_learning": (
    objective: "Xác định các hình mẫu và liên kết thống kê trong một luồng hình ảnh.",
    controls: "Hãy gõ các tùy chọn đại diện cho các chuỗi hoặc cặp xuất hiện cùng nhau.",
    walkthrough: [
      "Xem dòng các hình thể xuất hiện một cách ngẫu nhiên trên màn hình.",
      "Hình thể bên trong luôn xuất hiện cùng nhau theo cặp hoặc ba con.",
      "Trong giai đoạn thử nghiệm, hãy chọn cặp nào cảm thấy quen thuộc hơn.",
      "Chấp nhận những lựa chọn quen thuộc của bạn.",
    ],
    strategies: [
      "Hãy để não của bạn thu thập các chuỗi thụ động mà không phân tích quá nhiều các vật dụng cá nhân.",
      "Hãy tin tưởng vào cảm giác quen thuộc trong quá trình thử nghiệm.",
      "Quan sát sự chuyển đổi hình dạng chảy sát nhau.",
    ],
  ),
  "vocabulary_builder": (
    objective: "Chọn một từ đúng hoặc một biểu tượng cho từ vựng đã cho.",
    controls: "Gõ chính xác từ trong danh sách.",
    walkthrough: [
      "Đọc từ mục tiêu và mối quan hệ đã yêu cầu (synnonym hoặc antonym).",
      "Phân tích ý nghĩa của nhiều tùy chọn.",
      "Chọn từ thích hợp với mối quan hệ.",
      "Đương đầu.",
    ],
    strategies: [
      "Loại bỏ các tùy chọn có các phần của lời nói nhưng định nghĩa không liên quan.",
      "Hãy nghĩ về từ mục tiêu trong câu để nhớ lại bối cảnh của nó.",
      "Tiền tố và hậu tố có thể cho manh mối về ý nghĩa tích cực hoặc tiêu cực chung.",
    ],
  ),
  "vowel_reconstruct": (
    objective: "Điền vào các nguyên âm bị thiếu của một từ dựa trên các phụ âm còn lại và một phân loại ngữ pháp.",
    controls: "Gõ các nguyên âm theo đúng trình tự để hoàn thành từ.",
    walkthrough: [
      "Hãy lưu ý đầu mối ở trên cùng.",
      "Kiểm tra các phụ âm và khoảng trống.",
      "Gây ra từ phù hợp với phụ âm và loại.",
      "Đề nghị xác minh.",
    ],
    strategies: [
      "Hãy nghĩ đến những từ được cho là bắt đầu với phụ âm đầu tiên.",
      "Đặt các cặp nguyên âm phổ biến (như 'u', 'ee', 'ea') trong các dấu trống để thử chúng.",
      "Nói rằng khung xương phụ lớn tiếng để nghe từ tiềm năng phù hợp.",
    ],
  ),
  "water_sort": (
    objective: "Sắp xếp nước màu trong ống nghiệm cho đến khi mỗi ống chứa chỉ có một màu.",
    controls: "Gõ một ống để chọn nó, sau đó chạm vào một ống khác để đổ lớp nước trên cùng.",
    walkthrough: [
      "Hãy nhìn vào các lớp màu trong ống.",
      "Nhấn một ống với màu trên cùng bạn muốn đổ.",
      "Mở một ống dẫn điểm đến hoặc trống hoặc có cùng lớp màu trên cùng.",
      "Tiếp tục sắp xếp cho đến khi tất cả các màu được tách ra thành từng ống.",
    ],
    strategies: [
      "Giữ cho ít nhất một ống rỗng như một không gian chuyển tiếp tạm thời.",
      "Ống chế tạo chứa màu sắc đã ở gần đỉnh đầu tiên.",
      "Hãy lên kế hoạch các bước trước để tránh những khe trống.",
    ],
  ),
  "wisconsin_card_sorting": (
    objective: "Trích ra quy tắc ẩn để sắp xếp thẻ (theo màu, hình dạng, hay số) dựa trên phản hồi đúng đắn, và thích nghi khi quy tắc thay đổi.",
    controls: "Đập một trong bốn cọc để đặt thẻ của anh.",
    walkthrough: [
      "Xem lá bài được phân loại ở dưới cùng.",
      "Đặt nó lên một trong bốn chồng tham khảo.",
      "Nhận thông tin phản hồi về độ chính xác. Hãy dùng điều này để nhận diện nếu quy tắc sắp xếp hiện thời là dạng, màu hay số.",
      "Điều chỉnh cách sắp xếp của bạn để làm theo quy tắc này cho đến khi nó thay đổi một lần nữa.",
    ],
    strategies: [
      "Đừng hoảng sợ khi một quy tắc chính xác bắt đầu trở lại \"không chính xác\" - có nghĩa là quy tắc đã thay đổi.",
      "Luôn luôn thử nghiệm quy tắc một cách có hệ thống: màu sắc trước, sau đó hình dạng, sau đó số.",
      "Hãy nhớ điều luật cuối cùng để tránh lặp lại ngay sau khi đổi ca.",
    ],
  ),
  "word_association_recall": (
    objective: "Mục tiêu là ghi nhớ hai từ liên hệ và sau đó nhớ chính xác từ nào được liên kết với một từ được chỉ định.",
    controls: "Trong giai đoạn nghiên cứu, tap 'NEXT PAIR' hoặc 'SAT CALL' để tiếp tục. trong giai đoạn thu hồi, gõ chính xác từ danh sách đa loại.",
    walkthrough: [
      "Trong giai đoạn nghiên cứu, hãy nhìn vào hai từ trình bày từng bên và ghi nhớ cặp của họ.",
      "Tap 'NEXT PAIR' để xem tập tiếp theo, cho đến khi bạn hoàn thành tất cả 5 cặp và tap 'ST ALL'.",
      "Trong giai đoạn nhớ lại, một từ đích được hiển thị. Hãy chọn từ khớp với nó từ nhiều lựa chọn.",
      "Xác định chính xác tất cả 5 cặp để thắng trò chơi. Nếu bạn phạm lỗi, bạn phải bắt đầu lại giai đoạn học.",
    ],
    strategies: [
      "Tạo ra một hình ảnh tinh thần sinh động, kỳ lạ kết hợp hai từ (ví dụ, cho 'Apple - Ocean', hãy tưởng tượng một quả táo khổng lồ trôi nổi trên biển).",
      "Hãy nói lớn tiếng khi bạn nghiên cứu chúng để củng cố trí nhớ qua việc học thính giác.",
    ],
  ),
  "word_grid_connection": (
    objective: "Mục tiêu là nhóm một lưới 16 từ thành bốn loại gồm bốn từ liên quan nhau, trong một số hạn chế cố gắng.",
    controls: "Tap để chọn hay gỡ bỏ chính xác 4 từ khỏi lưới. Một khi chọn 4 từ, hãy nhấn nút « Nhóm phục tùng » xuất hiện ở dưới.",
    walkthrough: [
      "Quét 16 từ ồn ào trong lưới để tìm các kết nối hoặc chủ đề tiềm năng.",
      "Theo đúng 4 từ mà anh tin là thuộc về cùng một hạng mục.",
      "Nhấn nút « Tập đoàn chủ chốt » xuất hiện ở phía dưới.",
      "Nếu đúng, phân loại sẽ được giải quyết và gỡ bỏ khỏi lưới. Nếu không đúng, bạn mất một lần thử. Giải quyết tất cả 4 loại trước khi hết nỗ lực để giành chiến thắng.",
    ],
    strategies: [
      "Đừng đăng ký ngay lập tức nếu bạn thấy một sự kết nối; hãy chắc chắn là không có 5 hay 6 từ phù hợp với phân loại, có nghĩa là bạn cần phải giải quyết một loại chồng chéo khác trước.",
      "Nếu bạn bị mắc kẹt, hãy cố gắng tìm ra từ đặc biệt hay cụ thể nhất trên bảng và tìm ra nó phải kết nối với cái gì.",
    ],
  ),
  "word_ladder": (
    objective: "Mục tiêu là biến từ đầu thành từ cuối bằng cách thay đổi chỉ một chữ cái cùng một lúc, mỗi bước trung gian phải là một từ hợp lệ.",
    controls: "Dùng bàn phím trên màn hình để gõ từ nào thay đổi chính xác một chữ cái từ chữ trước. Nhấn nút Nhập để đệ trình hay DEL để sửa lỗi.",
    walkthrough: [
      "Xem từ bắt đầu và cuối cùng được hiển thị ở đầu trang.",
      "Dùng bàn phím để nhập một từ hợp lệ khác với từ dưới cùng của thang hiện tại bằng chính xác một chữ cái.",
      "Tap nhập để gửi từ này, nếu hợp lệ, nó sẽ được thêm vào thang.",
      "Tiếp tục xiềng xích cho đến khi bạn thành công trong việc bước vào từ cuối cùng để hoàn tất thang.",
    ],
    strategies: [
      "Hãy cố gắng suy nghĩ về từ cuối cùng trong trí để xem từ ngữ nào có thể liên quan đến nó.",
      "Thay nguyên âm trước nếu bạn bị mắc kẹt, vì nó mang lại sự linh hoạt nhất để tạo ra từ mới.",
    ],
  ),
  "word_mastermind": (
    objective: "Mục tiêu là đoán 4 chữ cái ẩn bằng cách nhập vào các dự đoán và sử dụng các Bulls (B) và Cows (C) phản hồi.",
    controls: "Sử dụng bàn phím trên màn hình để gõ một dự đoán 4 chữ cái và bấm nút nhập vào để đệ trình.",
    walkthrough: [
      "Nhập một từ bắt đầu bằng bàn phím và nhấn nút nhập.",
      "Xem lại các phản hồi được cung cấp bên cạnh dự đoán của bạn: 'B' ngụ ý một Bull (chính xác chữ cái ở vị trí đúng), và 'C' ngụ ý một con bò (chính xác chữ cái nhưng ở vị trí sai).",
      "Dùng lập luận này để suy đoán.",
      "Tiếp tục đoán cho đến khi bạn có 4 Bulls, tiết lộ từ mục tiêu trước khi bạn hết nỗ lực.",
    ],
    strategies: [
      "Dùng một từ bắt đầu với 4 chữ cái chung đặc biệt (như 'TER' hoặc 'LION') để tối đa hóa thông tin ban đầu.",
      "Nếu bạn nhận được một 'Cow', cố gắng di chuyển lá thư đến một vị trí khác trong dự đoán tiếp theo của bạn.",
    ],
  ),
  "word_scramble": (
    objective: "Mục tiêu là tháo gỡ các chữ cái để tìm ra từ đúng mục tiêu.",
    controls: "Hãy nhắp vào các nút văn bản trộn để đánh vần từ. Hãy dùng cái nút vùng ngược để sửa lỗi, cái nút tươi để rõ ràng hơn, và SUBMIT để kiểm tra câu trả lời của bạn.",
    walkthrough: [
      "Xem các chữ cái trộn được hiển thị ở đầu màn hình.",
      "Tâm trí sắp xếp lại các chữ cái để tìm ra từ gốc.",
      "Gõ các nút chữ cái từng cái một để đánh vần suy đoán của bạn trong các hộp nhập.",
      "Nếu đúng, anh thắng!",
    ],
    strategies: [
      "Tìm kiếm các tiền tố chung (như 're-', 'un-') hoặc hậu tố (như '-ing', '-d', '-tion') giữa các chữ cái.",
      "Hãy thử kết hợp giữa các phụ âm và nguyên âm thường đi cùng nhau (v. g., 'th', 'ch','ea'.",
    ],
  ),
  "word_search": (
    objective: "Mục tiêu là tìm tất cả các từ được liệt kê bên trong lưới chữ cái.",
    controls: "Kéo ngón tay qua các chữ cái trong lưới (thường, theo chiều dọc, hoặc chéo) để tô sáng và chọn một từ.",
    walkthrough: [
      "Xem lại danh sách 'WORDS to find' ở dưới cùng của màn hình.",
      "Quét lưới chữ cái ở trên để xác định chữ cái đầu tiên của một trong những từ này.",
      "Khi tìm thấy, hãy ấn và kéo ngón tay từ chữ thứ nhất đến chữ cuối cùng của chữ, rồi nhả ra.",
      "Tìm và làm nổi bật tất cả các từ trong danh sách để hoàn thành câu đố.",
    ],
    strategies: [
      "Tìm kiếm những chữ cái ít phổ biến nhất trong một từ (như Q, X, Z, K, hoặc V) thay vì bắt đầu với chữ cái thứ nhất.",
      "Quét hàng hoặc cột theo hàng một cách có hệ thống nếu bạn bị mắc kẹt.",
    ],
  ),
  "word_snake_trail": (
    objective: "Mục tiêu là lần theo đường dẫn liên tục của một từ bị ẩn trong một lưới chữ cái.",
    controls: "Gõ các tế bào chữ bên cạnh từng chữ cái một bắt đầu từ chữ cái đầu tiên để lần theo đường dẫn toàn bộ từ.",
    walkthrough: [
      "Đọc từ TARGET được hiển thị ở đầu màn hình.",
      "Xác định chữ bắt đầu trong lưới 4x4.",
      "Gõ chữ cái đầu, rồi gõ các chữ kế nhau để theo dõi từ đầy đủ.",
      "Thành công lần theo số từ đích để thắng trò chơi. Nếu bạn gõ sai phím, đường dẫn sẽ được đặt lại.",
    ],
    strategies: [
      "Trước khi gõ chữ cái đầu tiên, hãy nhìn toàn bộ con đường trong đầu để đảm bảo nó dẫn tới chữ cuối cùng.",
      "Hãy nhớ rằng con đường này có thể rắn ở bất cứ hướng nào bên cạnh (lên, xuống, bên trái, bên phải) nhưng không thể thăm lại một tế bào mà nó đã dùng rồi.",
    ],
  ),
  "word_surge": (
    objective: "Mục tiêu là để nhanh chóng xác định đồng âm hoặc atonyms cho các từ mục tiêu để đạt điểm trước khi đồng hồ chạy.",
    controls: "Hãy nhấn nút tùy chọn đúng từ bốn tùy chọn được hiển thị trong mạng lưới.",
    walkthrough: [
      "hãy nhìn vào dấu hiệu để xem bạn cần một SYNONYM hay ATNYM.",
      "Đọc từ mục tiêu lớn ở giữa màn hình.",
      "Nhanh chóng đánh giá bốn lựa chọn và gõ đúng lựa chọn.",
      "Lặp lại quá trình càng nhanh càng tốt để điền vào thanh tiến trình trước khi hết giờ.",
    ],
    strategies: [
      "Hãy kiểm tra kỹ từng chữ một cho mỗi chữ mới; nó có thể chuyển giữa SYNONYM và ANYM.",
      "Hãy hành động nhanh chóng nhưng tránh đoán mò bốc đồng, vì những sai sót này tốn nhiều thì giờ quý báu.",
    ],
  ),
  "word_wheel": (
    objective: "Mục tiêu là tìm những từ hợp lệ dùng những lá thư đã cung cấp, trong đó mỗi từ phải bao gồm chữ trung tâm.",
    controls: "Hãy gõ các nút chữ cái để đánh vần một từ, sử dụng nút backspace để sửa lỗi, và nhấn nút SUBMIT để nhập vào dự đoán của bạn.",
    walkthrough: [
      "Nhìn vào bánh xe, chú ý đặc biệt đến chữ trung tâm.",
      "Đánh vần một từ dùng các chữ cái đã cho (nemum 3 chữ cái) bằng cách gõ các nút chữ cái. Từ này phải chứa chữ cái trung tâm.",
      "Bắt lỗi chính tả để kiểm tra từ. Nếu nó đúng, nó sẽ được thêm vào danh sách các từ đã tìm thấy.",
      "Tìm số từ cần thiết để thắng trận đấu.",
    ],
    strategies: [
      "Cố gắng tìm ra tiền tố và hậu tố bạn có thể tạo với các chữ cái bên ngoài để gắn vào chữ cái trung tâm.",
      "Hãy tìm từ \"Pangram\" - một từ dùng tất cả 7 chữ cái được cung cấp trong vô lăng.",
    ],
  ),
  "counting_sheep": (
    objective: "Mục tiêu là đếm chính xác số con chiên di chuyển qua màn hình và tổng cộng lại.",
    controls: "Nhấn vào mức độ khó để bắt đầu. rồi dùng bàn phím để gõ số và gõ 'bập tắt trả lời'.",
    walkthrough: [
      "Chọn mức độ khó khăn (ít, vừa, hoặc khó) để bắt đầu trò chơi.",
      "Hãy chú ý đến màn hình và đếm những con đà điểu emojis khi chúng di chuyển từ trái sang phải.",
      "Khi tất cả các con chiên đã đi qua và màn hình nhập ra, hãy gõ tổng số mà bạn đếm vào trường văn bản.",
      "Nhấn nút trả lời để xác minh đếm.",
    ],
    strategies: [
      "Giữ mắt tập trung một chút để nhìn toàn bộ màn hình và tránh mất tích những con cừu đang di chuyển nhanh.",
      "Nếu chiên xuất hiện theo từng cụm, hãy cố nhóm chúng lại thành từng nhóm nhỏ (như 2 hoặc 3) tinh thần thay vì đếm từng nhóm một.",
    ],
  ),
  "counting_span": (
    objective: "Mục tiêu là đếm chính xác các mục tiêu trong mỗi chuỗi màn hình và sau đó nhớ lại tất cả những số đó theo thứ tự chính xác mà chúng xuất hiện.",
    controls: "Ấn nút số tương ứng với số đếm của bạn trong giai đoạn đếm. Sau đó, hãy dùng bảng số để nhập chuỗi số trong giai đoạn nhớ lại.",
    walkthrough: [
      "Trong giai đoạn đếm, hãy nhìn màn hình và đếm chỉ các đối tượng đích đã ghi rõ.",
      "Nhấn nút đúng số từ các tùy chọn ở dưới màn hình.",
      "Lặp lại quá trình này cho một chuỗi nhiều màn hình, nhớ đếm chính xác từ mỗi màn hình theo thứ tự.",
      "Trong giai đoạn nhớ lại, hãy sử dụng bảng số để nhập chính xác chuỗi số mà bạn đếm trên tất cả màn hình.",
    ],
    strategies: [
      "Hãy hình dung chuỗi số là một số lớn hơn (v. g., 3, 5, 2 trở thành 'Ba-Fify-Hai') để dễ nhớ hơn.",
      "Nhanh chóng quét các mục tiêu thay vì đếm từng hình dạng, và không để những người đánh lạc hướng phá vỡ sự tập trung của bạn.",
    ],
  ),
  "cross_section_slice": (
    objective: "Mục tiêu là để xác định chính xác hình dạng 2D mà kết quả là cắt một hình 3D với một máy bay.",
    controls: "Ấn nút tương ứng với hình 2 chiều chính xác ở dưới màn hình.",
    walkthrough: [
      "Quan sát khối 3D và máy bay được tô sáng cắt xuyên qua nó ở vùng quan sát chính.",
      "Hình dung ra hình dạng 2D cắt ngang được tạo ra chính xác khi máy bay chạm vào khối rắn.",
      "Xem các tùy chọn dạng 2D ở dưới màn hình.",
      "Nhấn vào tùy chọn khớp hình ảnh của bạn. Phải xác định đúng số phần bổ sung để thắng.",
    ],
    strategies: [
      "Hãy chú ý đến góc của máy bay cắt; một đường chéo cắt xuyên qua một ống trụ tạo ra hình bầu dục, chứ không phải hình tròn.",
      "Hãy tưởng tượng nhìn trực tiếp xuống máy bay cắt vuông góc với bề mặt của nó để thấy hình dạng 2D thực sự.",
    ],
  ),
  "crossword": (
    objective: "Mục tiêu là lấp đầy toàn bộ lưới bằng những từ chính xác dựa trên những manh mối đã cung cấp.",
    controls: "Hãy gõ một tế bào trong lưới để chọn nó và xem đầu mối của nó. Hãy dùng bàn phím trên màn hình để nhập chữ cái.",
    walkthrough: [
      "Mở một ô trống trong lưới ô chữ. Việc này làm nổi bật chữ (Across or Down) và hiển thị đầu mối tương ứng bên dưới lưới.",
      "Đọc đầu mối và dùng bàn phím trên màn hình để gõ câu trả lời. Lựa chọn sẽ tự động trước chữ kế.",
      "Gõ điện thoại lần nữa nếu bạn cần phải chuyển giữa các dấu vết giao nhau \"Across\" và ' Down'.",
      "Tiếp tục tìm manh mối cho đến khi toàn bộ lưới được lấp đầy.",
    ],
    strategies: [
      "Bắt đầu với những từ ngắn nhất hoặc những manh mối lấp đầy, vì chúng thường là những từ dễ nhất để giải và cung cấp chữ cái vượt qua cho những từ khó khăn hơn.",
      "Nếu bạn bị mắc kẹt trong một từ, chuyển sang các từ giao nhau để nhận được nhiều chữ cái hơn.",
    ],
  ),
};
