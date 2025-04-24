from data_access_layer.base_repository import BaseRepository

class BankStaffRepository(BaseRepository):
    def __init__(self):
        super().__init__('staff')

    def add_staff(self, staff_data):
        data = self.load_data()
        data.append(staff_data)
        self.save_data(data)

    def get_all_staff(self):
        return self.load_data()

    def get_staff_by_id(self, staff_id):
        data = self.load_data()
        return next((staff for staff in data if staff['staff_id'] == staff_id), None)

    def update_staff(self, staff_id, updated_data):
        data = self.load_data()
        for i, staff in enumerate(data):
            if staff.get('staff_id') == staff_id:
                data[i].update(updated_data)
                self.save_data(data)
                return True
        return False

    def delete_staff(self, staff_id):
        data = self.load_data()
        new_data = [staff for staff in data if staff['staff_id'] != staff_id]
        if len(new_data) != len(data):  # Means something was deleted
            self.save_data(new_data)
            return True
        return False

    def get_staff_by_credentials(self, bank_id, username, password):
        data = self.load_data()
        for staff in data:
            if (
                staff['bank_id'] == bank_id and
                staff['staff_username'] == username and
                staff['staff_password'] == password and
                staff['is_active']
            ):
                return staff
        return None
