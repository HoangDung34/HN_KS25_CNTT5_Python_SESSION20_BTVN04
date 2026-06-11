import logging

logging.basicConfig(
    filename="roster_app.log",
    level=logging.INFO,
    format="[%(asctime)s] - [%(levelname)s] - %(message)s"
)

roster = [
    {
        "player_id": "P01",
        "name": "Faker",
        "role": "Mid Lane",
        "salary": 5000.0,
        "status": "Active"
    },
    {
        "player_id": "P02",
        "name": "Oner",
        "role": "Jungle",
        "salary": 3500.0,
        "status": "Active"
    },
    {
        "player_id": "P03",
        "name": "Ruler",
        "role": "ADC",
        "salary": 6000.0,
        "status": "Benched" # Tuyển thủ dự bị
    }
]

def calculate_actual_pay(player):
    if player["status"] == "Benched":
        return player["salary"] * 0.5

    return player["salary"]

def display_roster(roster_list):
    logging.info("Coach viewed the team roster")

    if not roster_list:
        print("Đội hình hiện đang trống")
        return

    print("--- ĐỘI HÌNH RIKKEI ESPORTS ---")

    print(f"{'ID':<8} | {'Tên tuyển thủ':<20} | {'Vị trí':<15} | {'Lương':<12} | {'Trạng thái'}")

    print("-----------------------------------------------------------------------------------------------")

    for player in roster_list:
        status = player.get("status", "Unknown")

        name = player["name"]

        if status == "Benched":
            name += " [DỰ BỊ]"

        print(f"{player['player_id']:<8} | {name:<20} | {player['role']:<15} | {player['salary']:<12,.1f} | {status}")

def add_player(roster_list):
    print("--- CHIÊU MỘ TUYỂN THỦ MỚI ---")

    player_id = input("Nhập mã tuyển thủ: ").strip().upper()

    for player in roster_list:
        if player["player_id"] == player_id:
            print(f"Lỗi: Mã tuyển thủ {player_id} đã tồn tại")

            logging.warning(f"Failed to sign player - Duplicate player ID {player_id}")
            return

    name = input("Nhập tên tuyển thủ: ").title()
    role = input("Nhập vị trí thi đấu: ").title()

    while True:
        try:
            salary = float(input("Nhập mức lương hàng tháng: "))

            if salary <= 0:
                print("Lương phải là số dương. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("Lương phải là số. Vui lòng nhập lại.")

            logging.warning("Failed to sign player - Invalid salary input")

    roster_list.append({"player_id": player_id, "name": name, "role": role, "salary": salary, "status": "Active"})

    print(f"Thành công: Đã chiêu mộ tuyển thủ {name}")

    logging.info(f"Signed new player {name} with salary {salary}")

def update_player(roster_list):
    print("--- CẬP NHẬT LƯƠNG & TRẠNG THÁI THI ĐẤU ---")

    player_id = input("Nhập mã tuyển thủ cần cập nhật: ").strip().upper()
    flag = None

    for player in roster_list:
        if player["player_id"] == player_id:
            flag = player
            break

    if not flag:
        print(f"Không tìm thấy tuyển thủ mang mã {player_id}")

        logging.warning(f"Failed to update player - Player ID {player_id} not found")
        return

    print(f"Tuyển thủ: {flag['name']}")
    print(f"Vị trí: {flag['role']}")
    print(f"Lương hiện tại: {flag['salary']}")
    print(f"Trạng thái hiện tại: {flag['status']}")

    print("""
        1. Cập nhật lương
        2. Cập nhật trạng thái thi đấu
        3. Thoát
    """)

    choose = input("Chọn chức năng cập nhật (1-2): ")

    match choose:
        case "1":
            while True:
                try:
                    new_salary = float(input("Nhập mức lương mới: "))

                    if new_salary <= 0:
                        print("Lương phải là số dương")
                        continue

                    old_salary = flag["salary"]
                    flag["salary"] = new_salary

                    logging.info(f"Updated player {player_id} salary from {old_salary} to {new_salary}")

                    print(f"Thành công: Đã cập nhật lương cho tuyển thủ {player_id}")

                    break
                except ValueError:
                    print("Lương phải là số")
        case "2":
            print("""
            1. Active
            2. Benched
            3. Thoát
            """)

            status_choose = input("Nhập lựa chọn trạng thái (1-2): ")

            old_status = flag["status"]

            match status_choose:
                case "1":
                    flag["status"] = "Active"
                case "2":
                    flag["status"] = "Benched"
                case "3":
                    return
                case _:
                    print("Lựa chọn trạng thái không hợp lệ")
                    return

            logging.info(f"Updated player {player_id} status from {old_status} to {flag['status']}")

            print(f"Thành công: Đã cập nhật trạng thái cho tuyển thủ {player_id}")
        case "3":
            return
        case _:
            print("Lựa chọn không hợp lệ")
            return

def generate_payroll_report(roster_list):
    print("--- BÁO CÁO QUỸ LƯƠNG HÀNG THÁNG ---")

    if not roster_list:
        print("Đội hình hiện đang trống. Tổng quỹ lương: 0.0")
        return

    total = 0

    print(f"{'ID':<8} | {'Tên tuyển thủ':<15} | {'Trạng thái':<10} | {'Lương gốc':<12} | {'Lương thực nhận'}")

    print("--------------------------------------------------------------------------------------------------------------")

    try:
        for player in roster_list:
            actual_pay = calculate_actual_pay(player)
            total += actual_pay

            print(f"{player['player_id']:<8} | {player['name']:<15} | {player['status']:<10} | {player['salary']:<12,.1f} | {actual_pay:,.1f}")
    except KeyError as error:
        print("Lỗi: Một tuyển thủ đang bị thiếu dữ liệu.")

        logging.error(f"Missing key while generating payroll report: {error}")

        total = 0

    print("---------------------------------------------------------------------------------------------------------------")

    print(f"Tổng quỹ lương hàng tháng: {total:,.1f}")

    logging.info(f"Generated monthly payroll report. Total: {total}")

def main():
    while True:
        print("""
        ===== HỆ THỐNG QUẢN LÝ ĐỘI HÌNH RIKKEI ESPORTS =====
        1. Xem đội hình thi đấu hiện tại
        2. Chiêu mộ tuyển thủ mới
        3. Cập nhật lương & Trạng thái thi đấu
        4. Báo cáo quỹ lương hàng tháng
        5. Thoát hệ thống
        ==================================================
        """)

        choice = input("Chọn chức năng (1-5): ")

        match choice:
            case "1":
                display_roster(roster)
            case "2":
                add_player(roster)
            case "3":
                update_player(roster)
            case "4":
                generate_payroll_report(roster)
            case "5":
                logging.info("System shutdown.")
                print("Thoát chương trình")
                break
            case _:
                print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
