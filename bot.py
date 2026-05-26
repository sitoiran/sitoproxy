<?php
$token = "8009274939:AAHy-17cd-WkEMKEtYPlRgeys2oO_6Fg2Cc";
$admin_id = "8355555243";

$input = file_get_contents('php://input');
$update = json_decode($input);
if (!$update) exit;

$main_menu_inline = json_encode(['inline_keyboard' => [
    [['text' => '🟢 خرید اشتراک 🟢', 'callback_data' => 'main_buy']],
    [['text' => '👤 حساب کاربری', 'callback_data' => 'main_acc'], ['text' => '📞 پشتیبانی', 'callback_data' => 'main_sup']]
]]);

if (isset($update->message)) {
    $msg = $update->message; $chat_id = $msg->chat->id; $text = $msg->text;

    if ($text == "/start") {
        send_message($chat_id, "به فروشگاه فیلترشکن سی‌تو خوش آمدید.\nلطفاً یکی از گزینه‌های زیر را انتخاب کنید:", $main_menu_inline);
    } 
    elseif (isset($msg->photo)) {
        $ph_id = end($msg->photo)->file_id;
        
        $back_btn = json_encode(['inline_keyboard' => [
            [['text' => "🔙 بازگشت به منوی اصلی", 'callback_data' => "back_to_start"]]
        ]]);
        
        send_message($chat_id, "⏳ فیش دریافت شد. منتظر تایید مدیریت باشید.", $back_btn);
        
        $plan_file = "plan_{$chat_id}.txt";
        $current_plan = file_exists($plan_file) ? file_get_contents($plan_file) : "نامشخص";
        
        $adm_btns = json_encode(['inline_keyboard' => [[
            ['text' => "✅ تایید فیش", 'callback_data' => "conf_{$chat_id}"], 
            ['text' => "❌ رد فیش", 'callback_data' => "rej_$chat_id"]
        ]]]);
        send_photo($admin_id, $ph_id, "🔔 فیش جدید!\n🆔 آیدی: $chat_id\n💎 طرح درخواستی: $current_plan", $adm_btns);
    }
    
    if (isset($text) && $chat_id == $admin_id && isset($msg->reply_to_message)) {
        $reply_text = $msg->reply_to_message->text;
        if (strpos($reply_text, "شناسه:") !== false) {
            $u_id = trim(explode("\n", explode("شناسه:", $reply_text)[1])[0]);
            
            $plan_file = "plan_{$u_id}.txt";
            $current_plan = file_exists($plan_file) ? file_get_contents($plan_file) : "اشتراک معمولی";
            
            $today_shamsi = get_current_shamsi_date();
            
            $user_file = "user_{$u_id}.txt";
            $save_data = $current_plan . "|" . $text . "|" . $today_shamsi . "\n";
            file_put_contents($user_file, $save_data, FILE_APPEND);
            
            $msg_to_user = "✅ واریزی شما تایید شد!\n\n🚀 لینک اختصاصی شما:\n\n`$text` \n\n👆 روی لینک بزنید تا کپی شود.";
            
            $after_link_btns = json_encode(['inline_keyboard' => [
                [['text' => "🛠 برنامه لازم برای کانفیگ", 'callback_data' => "help_usage"], ['text' => "🛒 خرید اشتراک جدید", 'callback_data' => 'main_buy']],
                [['text' => "🔙 بازگشت به منوی اصلی", 'callback_data' => "back_to_start"]]
            ]]);
            
            send_message($u_id, $msg_to_user, $after_link_btns);
            send_message($admin_id, "✅ لینک با موفقیت برای کاربر $u_id ارسال شد و در تاریخچه حسابش ذخیره گردید.");
        }
    }
}

if (isset($update->callback_query)) {
    $cb = $update->callback_query; $data = $cb->data; $cid = $cb->message->chat->id; $mid = $cb->message->message_id;

    if ($data == "main_buy") {
        $inline = json_encode(['inline_keyboard' => [
            [['text' => "۳۰ مگ ◂ تست ۱۰ هزار تومان", 'callback_data' => "buy_test30mb_10-هزار-تومان"]],
            [['text' => "۱ گیگ ◂ ۲۰۰ هزار تومان دو کاربر", 'callback_data' => "buy_1gb2user_۲۰۰-هزار-تومان"]],
            [['text' => "۵ گیگ ◂ ۱ میلیون تومان دو کاربر", 'callback_data' => "buy_5gb2user_۱-میلیون-تومان"]],
            [['text' => "۱۰ گیگ ◂ ۲ میلیون تومان دو کاربر", 'callback_data' => "buy_10gb2user_۲-میلیون-تومان"]],
            [['text' => "۱۵ گیگ ◂ ۳ میلیون تومان دو کاربر", 'callback_data' => "buy_15gb2user_۳-میلیون-تومان"]],
            [['text' => "۲۰ گیگ ◂ ۴ میلیون تومان دو کاربر", 'callback_data' => "buy_20gb2user_۴-میلیون-تومان"]],
            [['text' => "🔙 بازگشت به منوی اصلی", 'callback_data' => "back_to_start"]]
        ]]);
        edit_message($cid, $mid, "🥇 لیست قیمت‌های اشتراک حجمی (یک‌ماهه):", $inline);
    }
    elseif ($data == "main_acc") {
        $username = isset($cb->from->username) ? "@" . $cb->from->username : "ثبت نشده";
        $user_file = "user_{$cid}.txt";
        $bought_links = "";
        $has_history = false;
        
        if (file_exists($user_file) && filesize($user_file) > 0) {
            $links_array = file($user_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            $counter = 1;
            foreach ($links_array as $line) {
                if (strpos($line, "|") !== false) {
                    $parts = explode("|", $line);
                    $plan_name = $parts[0]; 
                    $link_val = $parts[1];  
                    $date_val = isset($parts[2]) ? " 📅 تاریخ: " . $parts[2] : "";
                    
                    $bought_links .= "🔑 اشتراک شماره $counter : $plan_name$date_val\n`$link_val` \n\n";
                } else {
                    $bought_links .= "🔑 اشتراک شماره $counter :\n`$line` \n\n";
                }
                $counter++;
            }
            $has_history = true;
        } else {
            $bought_links = "❌ شما هنوز هیچ اشتراکی خریداری نکرده‌اید.";
        }
        
        $acc_text = "👤 حساب کاربری شما:\n\n💎 نام کاربری: $username\n🆔 آیدی عددی: `$cid` \n📍 وضعیت: آماده خرید\n\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n" .
                    "📦 لیست اشتراک‌های خریداری شده شما:\n\n" . $bought_links . 
                    "💡 *روی هر لینک بزنید به صورت خودکار کپی می‌شود.*";
                    
        $acc_buttons = [];
        if ($has_history) {
            $acc_buttons[] = [['text' => "🗑 حذف اشتراک‌ها", 'callback_data' => "confirm_clear"], ['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]];
        } else {
            $acc_buttons[] = [['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]];
        }
                    
        edit_message($cid, $mid, $acc_text, json_encode(['inline_keyboard' => $acc_buttons]));
    }
    elseif ($data == "confirm_clear") {
        // نمایش پیام تایید دو مرحله‌ای با علامت خطر و دکمه بله و خیر
        $warn_text = "⚠️ **هشدار مهم!**\n\nبا حذف اشتراک‌ها تمام لینک کانفیگ‌های شما حذف می‌شود و دیگر قابل بازگشت نیست.\n\nآیا مطمئن هستید؟";
        $warn_btns = json_encode(['inline_keyboard' => [
            [['text' => "✅ بله، مطمئنم", 'callback_data' => "clear_history_final"], ['text' => "❌ خیر، بازگشت", 'callback_data' => "main_acc"]]
        ]]);
        edit_message($cid, $mid, $warn_text, $warn_btns);
    }
    elseif ($data == "clear_history_final") {
        $user_file = "user_{$cid}.txt";
        if (file_exists($user_file)) {
            unlink($user_file);
        }
        call_api("answerCallbackQuery", ['callback_query_id' => $cb->id, 'text' => "🗑 تاریخچه خرید شما با موفقیت پاک شد!", 'show_alert' => true]);
        
        $username = isset($cb->from->username) ? "@" . $cb->from->username : "ثبت نشده";
        $acc_text = "👤 حساب کاربری شما:\n\n💎 نام کاربری: $username\n🆔 آیدی عددی: `$cid` \n📍 وضعیت: آماده خرید\n\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n" .
                    "📦 لیست اشتراک‌های خریداری شده شما:\n\n❌ شما هنوز هیچ اشتراکی خریداری نکرده‌اید.";
        edit_message($cid, $mid, $acc_text, json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]]]]));
    }
    elseif ($data == "main_sup") {
        edit_message($cid, $mid, "💎 پشتیبانی سی‌تو: @vpnsito\n\nسوالات و مشکلات خود را با ما در میان بگذارید.", json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => "back_to_start"]]]]));
    }
    elseif ($data == "back_to_start") {
        edit_message($cid, $mid, "به فروشگاه فیلترشکن سی‌تو خوش آمدید.\nیکی از گزینه‌های زیر را انتخاب کنید:", $main_menu_inline);
    }
    elseif ($data == "help_usage") {
        $app_list = "✅ اشتراک‌های ما تمام برنامه‌های زیر رو پشتیبانی می‌کنه:\n\n" .
                    "🟢 V2RAY\n" .
                    "🟢 V2BOX\n" .
                    "🟢 V2RAY NG\n" .
                    "🟢 V2RAY tun\n" .
                    "🟢 Hiddify\n" .
                    "🟢 Happ";
        send_message($cid, $app_list, $main_menu_inline);
    }
    elseif (strpos($data, "buy_") !== false) {
        $ex = explode("_", $data); 
        $plan_code = $ex[1]; 
        $price = str_replace("-", " ", $ex[2]);
        
        $name = "اشتراک معمولی";
        if ($plan_code == "test30mb") $name = "۳۰ مگ تست";
        elseif ($plan_code == "1gb2user") $name = "۱ گیگ یکماه دوکاربر";
        elseif ($plan_code == "5gb2user") $name = "۵ گیگ یکماه دوکاربر";
        elseif ($plan_code == "10gb2user") $name = "۱۰ گیگ یکماه دوکاربر";
        elseif ($plan_code == "15gb2user") $name = "۱۵ گیگ یکماه دوکاربر";
        elseif ($plan_code == "20gb2user") $name = "۲۰ گیگ یکماه دوکاربر";
        
        file_put_contents("plan_{$cid}.txt", $name);
        
        $pay_text = "✅ **طرح انتخاب شده:** $name\n💰 **مبلغ قابل پرداخت:** $price\n\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n💳 شماره کارت جهت واریز:\n`6219861814211347`\n👤 **بنام:** مهین سراقی\n" .
                    "➖➖➖➖➖➖➖➖➖➖\n\n💡 *برای کپی آسان، روی شماره کارت بالا بزنید.*\n\n👇 **لطفاً پس از واریز، تصویر فیش را اینجا ارسال کنید:**";
        
        edit_message($cid, $mid, $pay_text, json_encode(['inline_keyboard' => [[['text' => "🔙 بازگشت", 'callback_data' => "main_buy"]]]]));
    }
    elseif (strpos($data, "conf_") !== false) {
        $u_id = str_replace("conf_", "", $data);
        send_message($admin_id, "لینک را روی این پیام ریپلای کنید:\nشناسه: $u_id");
    }
    elseif (strpos($data, "rej_") !== false) {
        send_message(str_replace("rej_", "", $data), "❌ فیش تایید نشد.");
    }
    
    call_api("answerCallbackQuery", ['callback_query_id' => $cb->id]);
}

function send_message($c, $t, $m = null) { return call_api("sendMessage", ['chat_id' => $c, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function send_photo($c, $p, $cap, $m = null) { return call_api("sendPhoto", ['chat_id' => $c, 'photo' => $p, 'caption' => $cap, 'reply_markup' => $m]); }
function edit_message($c, $mid, $t, $m = null) { return call_api("editMessageText", ['chat_id' => $c, 'message_id' => $mid, 'text' => $t, 'parse_mode' => 'Markdown', 'reply_markup' => $m]); }
function call_api($method, $post) {
    global $token; $u = "https://api.telegram.org/bot$token/$method";
    $ch = curl_init(); curl_setopt($ch, CURLOPT_URL, $u); curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post); curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $r = curl_exec($ch); curl_close($ch); return $r;
}

function get_current_shamsi_date() {
    $timestamp = time();
    $g_y = intval(date('Y', $timestamp));
    $g_m = intval(date('m', $timestamp));
    $g_d = intval(date('d', $timestamp));

    $g_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    if (($g_y % 4 == 0 && $g_y % 100 != 0) || ($g_y % 400 == 0)) {
        $g_days_in_month[1] = 29;
    }

    $g_day_no = 0;
    for ($i = 0; $i < $g_m - 1; $i++) {
        $g_day_no += $g_days_in_month[$i];
    }
    $g_day_no += $g_d - 1;

    $jy = $g_y - 621;
    $j_day_no = $g_day_no - 79;

    if ($j_day_no < 0) {
        $jy--;
        $j_day_no += (($jy % 4 == 0 && $jy % 100 != 0) || ($jy % 400 == 0)) ? 366 : 365;
    }

    if ($j_day_no < 186) {
        $jm = intval($j_day_no / 31) + 1;
        $jd = ($j_day_no % 31) + 1;
    } else {
        $j_day_no -= 186;
        $jm = intval($j_day_no / 30) + 7;
        $jd = ($j_day_no % 30) + 1;
    }

    return sprintf("%04d/%02d/%02d", $jy, $jm, $jd);
}
?>
